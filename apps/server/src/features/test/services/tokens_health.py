from typing import Any
from src.conf.db import db_trx
from src.features.auth.middleware.register import RegisterFormT
from src.features.test.lib.register_user import handle_user_lib
from src.lib.data_structure import parse_id
from src.lib.tokens.cbc_hmac import (
    check_cbc_hmac,
    gen_cbc_hmac,
)
from src.lib.tokens.jwe import check_jwe, gen_jwe
from src.lib.tokens.jwt import gen_jwt, verify_jwt
from src.models.token import GenTokenReturnT, TokenT


async def tokens_health_svc(user_data: RegisterFormT) -> Any:
    async with db_trx() as trx:

        us = await handle_user_lib(user_data, trx)
        parsed_us_id: str = parse_id(us.id)

        access_token: str = gen_jwt({"user_id": parsed_us_id})
        result_jwe: GenTokenReturnT = await gen_jwe(
            user_id=parsed_us_id, trx=trx
        )

        result_cbc_hmac: GenTokenReturnT = await gen_cbc_hmac(
            payload={"user_id": parsed_us_id},
            hdr={
                "token_t": TokenT.MANAGE_ACC,
            },
            trx=trx,
        )

        return {
            "new_user": us.to_d(exclude_keys=["password"]),
            "access_token": access_token,
            "access_token_decoded": verify_jwt(
                access_token,
            ),
            "refresh_token": result_jwe["client_token"],
            "refresh_token_db": result_jwe["server_token"].to_d(),
            "refresh_token_decrypted": (
                await check_jwe(result_jwe["client_token"], trx)
            )["decrypted"],
            "cbc_hmac_token": result_cbc_hmac["client_token"],
            "cbc_hmac_db": result_cbc_hmac["server_token"].to_d(),
            "cbc_hmac_token_len": len(result_cbc_hmac["client_token"]),
            "cbc_hmac_token_parts_len": list(
                map(len, (result_cbc_hmac["client_token"]).split("."))
            ),
            "cbc_hmac_decrypted": (
                await check_cbc_hmac(result_cbc_hmac["client_token"], trx=trx)
            )["decrypted"],
        }
