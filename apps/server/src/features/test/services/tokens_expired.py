from src.conf.db import db_trx
from src.features.auth.middleware.register import RegisterFormT
from src.features.test.lib.register_user import handle_user_lib
from src.lib.db.idx import clear_old_tokens
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.lib.tokens.combo import gen_tokens_session
from src.models.token import GenTokenReturnT, TokenT


async def tokens_expired_svc(user_data: RegisterFormT) -> dict:
    async with db_trx() as trx:
        us = await handle_user_lib(user_data, trx)

        await clear_old_tokens(trx, us.id)

        access_token, result_jwe = await gen_tokens_session(
            user_id=us.id, trx=trx, reverse=True
        )

        result_cbc_hmac: GenTokenReturnT = await gen_cbc_hmac(
            user_id=us.id,
            hdr={
                "token_t": TokenT.CONF_EMAIL,
            },
            trx=trx,
            reverse=True,
        )

        return {
            "access_token": access_token,
            "refresh_token": result_jwe["client_token"],
            "cbc_hmac_token": result_cbc_hmac["client_token"],
        }
