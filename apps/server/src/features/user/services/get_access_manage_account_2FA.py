from src.conf.db import db_trx
from src.lib.combo.TFA import check_2FA_lib
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT


async def get_access_manage_account_svc(
    res_combo: ComboCheckJwtCbcBodyReturnT,
) -> None:

    async with db_trx() as trx:
        res_check = await check_2FA_lib(trx, res_combo)
