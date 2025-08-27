from src.conf.db import db_trx
from src.lib.db.idx import del_token_by_t, get_us_by_id
from src.lib.etc import grab
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT
from src.models.token import TokenT


async def login_topt_svc(
    result_combo: ComboCheckJwtCbcBodyReturnT,
) -> TokensSessionsReturnT:

    async with db_trx() as trx:
        us = await get_us_by_id(trx=trx, us_id=grab(result_combo, "user_id"))

        us.check_totp(user_code=result_combo["body"]["totp_code"])

        tokens_session: TokensSessionsReturnT = await gen_tokens_session(
            user_id=us.id, trx=trx
        )

        await del_token_by_t(trx=trx, token_t=TokenT.LOGIN_2FA, us_id=us.id)
        return tokens_session
