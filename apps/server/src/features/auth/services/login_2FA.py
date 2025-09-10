from src.conf.db import db_trx
from src.lib.combo.TFA import check_2FA_lib
from src.lib.data_structure.etc import dest_d
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT


class Login2FASvcReturnT(TokensSessionsReturnT):
    backup_codes_left: int | None


async def login_2FA_svc(
    result_combo: ComboCheckJwtCbcBodyReturnT,
) -> Login2FASvcReturnT:
    async with db_trx() as trx:
        us, backup_codes_left = dest_d(
            d=await check_2FA_lib(trx, result_combo, delete_tok_on_check=True),
            keys=["user", "backup_codes_left"],
        )

        res_token = await gen_tokens_session(
            trx=trx,
            user_id=us.id,
        )

        return {
            "backup_codes_left": backup_codes_left,
            **res_token,
        }
