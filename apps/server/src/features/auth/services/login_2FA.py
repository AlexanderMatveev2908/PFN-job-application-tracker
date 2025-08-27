from src.conf.db import db_trx
from src.lib.data_structure import dest_d
from src.lib.db.idx import del_token_by_t
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.lib.validators.idx import check_2FA_lib
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT
from src.models.token import TokenT


class Login2FASvcReturnT(TokensSessionsReturnT):
    backup_codes_left: int | None


async def login_2FA_svc(
    result_combo: ComboCheckJwtCbcBodyReturnT,
) -> Login2FASvcReturnT:
    async with db_trx() as trx:
        us, backup_codes_left = dest_d(
            d=await check_2FA_lib(trx, result_combo),
            keys=["user", "backup_codes_left"],
        )

        await del_token_by_t(trx=trx, us_id=us.id, token_t=TokenT.LOGIN_2FA)

        res_token = await gen_tokens_session(
            trx=trx,
            user_id=us.id,
        )

        return {
            "backup_codes_left": backup_codes_left,
            **res_token,
        }
