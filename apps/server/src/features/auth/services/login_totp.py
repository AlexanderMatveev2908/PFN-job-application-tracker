from sqlalchemy import text
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.db.idx import get_us_by_id
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT
from src.models.token import TokenT


async def login_topt_svc(
    result_combo: ComboCheckJwtCbcBodyReturnT,
) -> TokensSessionsReturnT:

    async with db_trx() as trx:
        us = await get_us_by_id(
            trx=trx, us_id=result_combo["cbc_hmac_result"]["user_d"]["id"]
        )

        if not us.check_totp(user_code=result_combo["body"]["totp_code"]):
            raise ErrAPI(msg="TOTP_CODE_INVALID", status=401)

        tokens_session: TokensSessionsReturnT = await gen_tokens_session(
            user_id=result_combo["cbc_hmac_result"]["user_d"]["id"], trx=trx
        )

        await trx.execute(
            text(
                """
                DELETE FROM tokens
                    WHERE user_id = :user_id
                    AND token_t = :token_t
                """
            ),
            {
                "user_id": result_combo["cbc_hmac_result"]["user_d"]["id"],
                "token_t": TokenT.LOGIN_2FA.value,
            },
        )

        return tokens_session
