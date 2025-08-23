from typing import Any
from src.conf.db import db_trx
from src.features.auth.middleware.register import RegisterFormT
from src.features.test.lib.register_user import handle_user_lib
from src.lib.db.idx import clear_old_tokens
from src.lib.tokens.cbc_hmac import (
    check_cbc_hmac_with_us,
    gen_cbc_hmac,
)
from src.lib.tokens.combo import gen_tokens_session
from src.lib.tokens.jwe import check_jwe
from src.lib.tokens.jwt import check_jwt_lib
from src.models.token import GenTokenReturnT, TokenT


async def tokens_health_svc(
    user_data: RegisterFormT, token_t: TokenT, reverse: bool = False
) -> Any:
    async with db_trx() as trx:

        us = await handle_user_lib(user_data, trx)

        await clear_old_tokens(trx, us.id)

        access_token, result_jwe = await gen_tokens_session(
            user_id=us.id, trx=trx, reverse=reverse
        )

        result_cbc_hmac: GenTokenReturnT = await gen_cbc_hmac(
            user_id=us.id,
            token_t=token_t,
            trx=trx,
            reverse=reverse,
        )

        base_res = {
            "access_token": access_token,
            "refresh_token": result_jwe["client_token"],
            "cbc_hmac_token": result_cbc_hmac["client_token"],
        }

        if reverse:
            return base_res

        return {
            **base_res,
            "new_user": us.to_d(exclude_keys=["password"]),
            "access_token_decoded": check_jwt_lib(
                access_token,
            ),
            "refresh_token_db": result_jwe["server_token"].to_d(),
            "refresh_token_decrypted": (
                await check_jwe(result_jwe["client_token"], trx)
            )["decrypted"],
            "cbc_hmac_db": result_cbc_hmac["server_token"].to_d(),
            "cbc_hmac_decrypted": (
                await check_cbc_hmac_with_us(
                    result_cbc_hmac["client_token"], trx=trx, token_t=token_t
                )
            )["decrypted"],
        }
