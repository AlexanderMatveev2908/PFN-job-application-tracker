from src.conf.db import db_trx
from src.lib.db.idx import del_token_by_t, get_us_by_id
from src.lib.etc import grab
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT
from src.models.token import TokenT


class Login2FASvcReturnT(TokensSessionsReturnT):
    backup_codes_left: int | None


async def login_2FA_svc(
    result_combo: ComboCheckJwtCbcBodyReturnT,
) -> Login2FASvcReturnT:
    async with db_trx() as trx:
        us = await get_us_by_id(trx, grab(result_combo, "user_id"))
        backup_codes_left: int | None = None

        if totp_code := grab(result_combo, "totp_code", parent="body"):
            us.check_totp(totp_code)
        elif backup_code := grab(result_combo, "backup_code"):
            backup_codes_left = (await us.check_backup_code(trx, backup_code))[
                "backup_codes_left"
            ]

        await del_token_by_t(trx=trx, us_id=us.id, token_t=TokenT.LOGIN_2FA)

        res_token = await gen_tokens_session(
            trx=trx,
            user_id=us.id,
        )

        return {
            "backup_codes_left": backup_codes_left,
            **res_token,
        }
