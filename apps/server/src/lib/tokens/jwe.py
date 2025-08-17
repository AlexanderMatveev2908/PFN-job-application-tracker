import asyncio
from typing import Any, cast
from jose import jwe
from sqlalchemy import select

from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.lib.algs.hmac import hash_db_hmac
from src.lib.data_structure import b_to_d, b_to_h, d_to_b, h_to_b
from src.lib.etc import calc_exp, lt_now
from src.lib.logger import clg
from src.models.token import (
    AlgT,
    CheckTokenReturnT,
    GenTokenReturnT,
    Token,
    TokenT,
)
from sqlalchemy.ext.asyncio import AsyncSession

env_var = get_env()

K_ALG = "RSA-OAEP-256"
P_ALG = "A256GCM"


async def gen_jwe(
    user_id: str, trx: AsyncSession, reverse: bool = False, **kwargs: Any
) -> GenTokenReturnT:
    payload = {"user_id": user_id, **kwargs}
    payload["exp"] = calc_exp("1d", reverse)

    enc_bytes: bytes = await asyncio.to_thread(
        jwe.encrypt,
        d_to_b(payload),
        h_to_b(env_var.jwe_public),
        algorithm=K_ALG,
        encryption=P_ALG,
    )

    refresh_db = Token(
        user_id=user_id,
        alg=AlgT.RSA_OAEP_256_A256GCM,
        exp=calc_exp("1d"),
        token_t=TokenT.REFRESH,
        hashed=hash_db_hmac(enc_bytes),
    )

    trx.add(refresh_db)
    await trx.flush([refresh_db])
    await trx.refresh(refresh_db)

    return {"client_token": b_to_h(enc_bytes), "server_token": refresh_db}


async def check_jwe(token: str, trx: AsyncSession) -> CheckTokenReturnT:

    try:
        stm = select(Token).where(Token.hashed == hash_db_hmac(h_to_b(token)))

        result = (await trx.execute(stm)).scalar_one_or_none()

        if not result:
            raise ErrAPI(msg="REFRESH_TOKEN_NOT_FOUND", status=401)

        token_d = result.to_d()

        if lt_now(token_d["exp"]):
            raise ErrAPI(msg="REFRESH_TOKEN_EXPIRED", status=401)

        decrypted_bytes = await asyncio.to_thread(
            jwe.decrypt, h_to_b(token), h_to_b(env_var.jwe_private)
        )

        payload = b_to_d(cast(bytes, decrypted_bytes))

        return {"decrypted": payload, "token_d": token_d}

    except ErrAPI:
        raise

    except Exception as err:
        clg(err, ttl="invalid token")
        raise ErrAPI(msg="REFRESH_TOKEN_INVALID", status=401)
