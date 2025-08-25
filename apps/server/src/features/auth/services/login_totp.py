from typing import cast

from sqlalchemy import text
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.TFA.totp import check_totp
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT
from src.models.token import TokenT


async def login_topt_svc(
    result_combo: ComboCheckJwtCbcBodyReturnT,
) -> TokensSessionsReturnT:
    result_totp = check_totp(
        secret=cast(
            str, result_combo["cbc_hmac_result"]["user_d"]["totp_secret"]
        ),
        user_code=result_combo["body"]["totp_code"],
    )

    if not result_totp:
        raise ErrAPI(msg="TOTP_INVALID", status=401)

    async with db_trx() as trx:
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
