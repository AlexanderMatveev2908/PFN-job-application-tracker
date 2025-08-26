from typing import TypedDict
from sqlalchemy import text
from src.conf.db import db_trx
from src.lib.TFA.backup import check_backup_code
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

        result_backup_code = await check_backup_code(
            trx,
            us_id=result_combo["cbc_hmac_result"]["user_d"]["id"],
            backup_code=result_combo["body"]["backup_code"],
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

        result_tokens: TokensSessionsReturnT = await gen_tokens_session(
            trx=trx,
            user_id=result_combo["cbc_hmac_result"]["user_d"]["id"],
        )

        return {
            "result_tokens": result_tokens,
            "backup_codes_left": result_backup_code["backup_codes_left"],
        }
