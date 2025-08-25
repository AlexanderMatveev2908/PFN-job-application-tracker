from typing import Any
from src.conf.db import db_trx
from src.features.auth.middleware.register import RegisterFormT
from src.features.test.lib.register_user import handle_user_lib
from src.lib.db.idx import clear_old_tokens
from src.lib.tokens.cbc_hmac import (
    gen_cbc_hmac,
)
from src.lib.tokens.combo import gen_tokens_session
from src.models.token import GenTokenReturnT, TokenT


async def tokens_health_svc(
    user_data: RegisterFormT,
    token_t: TokenT,
    reverse: bool = False,
    expired: list[str] = [],
) -> Any:
    async with db_trx() as trx:

        us = await handle_user_lib(user_data, trx)

        await clear_old_tokens(trx, us.id)

        result_tokens = await gen_tokens_session(
            user_id=us.id, trx=trx, reverse=reverse, expired=expired
        )

        result_cbc_hmac: GenTokenReturnT = await gen_cbc_hmac(
            user_id=us.id,
            token_t=token_t,
            trx=trx,
            reverse=reverse or "cbc_hmac" in expired,
        )

        return {
            "access_token": result_tokens["access_token"],
            "refresh_token": result_tokens["result_jwe"]["client_token"],
            "cbc_hmac_token": result_cbc_hmac["client_token"],
        }
