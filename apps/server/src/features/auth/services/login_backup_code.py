from typing import TypedDict, cast

from sqlalchemy import select, text
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.hashing.idx import check_argon
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT
from src.models.backup_code import BackupCode
from src.models.token import TokenT


class LoginBackupCodeSvcReturnT(TypedDict):
    result_tokens: TokensSessionsReturnT
    backup_codes_left: int


async def login_backup_code_svc(
    result_combo: ComboCheckJwtCbcBodyReturnT,
) -> LoginBackupCodeSvcReturnT:
    async with db_trx() as trx:

        backup_codes = cast(
            list[BackupCode],
            (
                await trx.execute(
                    select(BackupCode).from_statement(
                        text(
                            """
                            SELECT *
                                FROM backup_codes bc
                                WHERE bc.user_id = :user_id
                            """
                        )
                    ),
                    {
                        "user_id": result_combo["cbc_hmac_result"]["user_d"][
                            "id"
                        ]
                    },
                )
            )
            .scalars()
            .all(),
        )

        if not backup_codes:
            raise ErrAPI(msg="user has no backup codes", status=401)

        found_code: BackupCode | None = None

        for bc in backup_codes:
            if await check_argon(
                hashed=bc.code,
                plain=result_combo["body"]["backup_code"],
            ):
                found_code = bc
                break

        if not found_code:
            raise ErrAPI(msg="BACKUP_CODE_INVALID", status=401)

        await trx.delete(found_code)

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
            "backup_codes_left": len(backup_codes) - 1,
        }
