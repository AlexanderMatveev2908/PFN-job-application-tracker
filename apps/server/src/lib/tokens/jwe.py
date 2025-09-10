import asyncio
from typing import Any, cast
import uuid
from jose import jwe
from sqlalchemy import select

from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.lib.algs.hmac import hash_db_hmac
from src.lib.data_structure.etc import b_to_d, b_to_h, d_to_b, h_to_b
from src.lib.data_structure.parsers import parse_id
from src.lib.db.idx import del_token_by_t, get_us_by_id
from src.lib.etc import calc_exp, lt_now
from src.models.token import (
    AlgT,
    CheckTokenReturnT,
    CheckTokenWithUsReturnT,
    GenTokenReturnT,
    Token,
    TokenDct,
    TokenT,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import UserDcT

env_var = get_env()

K_ALG = "RSA-OAEP-256"
P_ALG = "A256GCM"


async def gen_jwe(
    user_id: str | uuid.UUID,
    trx: AsyncSession,
    reverse: bool = False,
    **kwargs: Any,
) -> GenTokenReturnT:

    parsed_id: str = parse_id(user_id)

    await del_token_by_t(
        trx,
        parsed_id,
        TokenT.REFRESH,
    )

    payload = {"user_id": parsed_id, **kwargs}

    enc_bytes: bytes = await asyncio.to_thread(
        jwe.encrypt,
        d_to_b(payload),
        h_to_b(env_var.jwe_public),
        algorithm=K_ALG,
        encryption=P_ALG,
    )

    refresh_db = Token(
        user_id=parsed_id,
        alg=AlgT.RSA_OAEP_256_A256GCM,
        exp=calc_exp("30m", reverse),
        token_t=TokenT.REFRESH,
        hashed=hash_db_hmac(enc_bytes),
    )

    trx.add(refresh_db)
    await trx.flush([refresh_db])
    await trx.refresh(refresh_db)

    return {"client_token": b_to_h(enc_bytes), "server_token": refresh_db}


async def check_jwe_lib(trx: AsyncSession, token: str) -> CheckTokenReturnT:
    try:
        token_b = h_to_b(token)

        stm = select(Token).where(Token.hashed == hash_db_hmac(token_b))

        existing = (await trx.execute(stm)).scalar_one_or_none()

        if not existing:
            raise ErrAPI(msg="jwe_not_found", status=401)

        if lt_now(existing.exp):
            await trx.delete(existing)
            raise ErrAPI(msg="jwe_expired", status=401)

        decrypted_bytes = await asyncio.to_thread(
            jwe.decrypt, token_b, h_to_b(env_var.jwe_private)
        )

        payload = b_to_d(
            cast(bytes, decrypted_bytes),
            err_status=401,
            err_msg="jwe_invalid_format",
        )

        return {
            "decrypted": payload,
            "token_d": cast(TokenDct, existing.to_d()),
        }

    except ErrAPI:
        raise

    except Exception:
        raise ErrAPI(msg="jwe_invalid", status=401)


async def check_jwe_with_us(
    token: str, trx: AsyncSession
) -> CheckTokenWithUsReturnT:

    result_jwe = await check_jwe_lib(trx=trx, token=token)

    us = await get_us_by_id(trx, result_jwe["decrypted"]["user_id"])

    return {
        **result_jwe,
        "user_d": cast(UserDcT, us.to_d()),
    }
