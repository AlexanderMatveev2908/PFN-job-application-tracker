import asyncio
from typing import Any, TypedDict, cast
from jose import jwe

from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.lib.algs.hmac import hash_db_hmac
from src.lib.data_structure import b_to_d, b_to_h, d_to_b, h_to_b
from src.lib.etc import calc_exp, lt_now
from src.lib.logger import clg
from src.models.token import AlgT, Token, TokenT
from sqlalchemy.ext.asyncio import AsyncSession

env_var = get_env()

K_ALG = "RSA-OAEP-256"
P_ALG = "A256GCM"


class JweReturnT(TypedDict):
    refresh_client: str
    refresh_server: Token


async def gen_jwe(
    user_id: str, trx: AsyncSession, reverse: bool = False, **kwargs: Any
) -> JweReturnT:
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

    return {"refresh_client": b_to_h(enc_bytes), "refresh_server": refresh_db}


async def check_jwe(token: str) -> dict | None:

    try:
        decrypted_bytes = await asyncio.to_thread(
            jwe.decrypt, h_to_b(token), h_to_b(env_var.jwe_private)
        )

        payload = b_to_d(cast(bytes, decrypted_bytes))

        if lt_now(payload["exp"]):
            raise ErrAPI(msg="REFRESH_TOKEN_EXPIRED", status=401)

        return payload

    except ErrAPI:
        raise

    except Exception as err:
        clg(err, ttl="invalid token")
        raise ErrAPI(msg="REFRESH_TOKEN_INVALID", status=401)
