from typing import TypedDict
from sqlalchemy import text
from src.conf.db import db_trx
from src.lib.db.idx import del_token_by_t, get_us_by_id
from src.lib.etc import grab
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT
from src.models.token import TokenT


class LoginBackupCodeSvcReturnT(TypedDict):
    result_tokens: TokensSessionsReturnT
    backup_codes_left: int


async def login_backup_code_svc(
    result_combo: ComboCheckJwtCbcBodyReturnT,
) -> LoginBackupCodeSvcReturnT:
    async with db_trx() as trx:

        us = await get_us_by_id(trx, grab(result_combo, "user_id"))

        result_backup_code = await us.check_backup_code(
            trx, grab(result_combo, "backup_code")
        )

        await del_token_by_t(trx=trx, us_id=us.id, token_t=TokenT.LOGIN_2FA)

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

        result_tokens: TokensSessionsReturnT = await gen_tokens_session(
            trx=trx,
            user_id=result_combo["cbc_hmac_result"]["user_d"]["id"],
        )

        return {
            "result_tokens": result_tokens,
            "backup_codes_left": result_backup_code["backup_codes_left"],
        }
