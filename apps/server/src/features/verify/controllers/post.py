from fastapi import Depends, Request
from fastapi.responses import JSONResponse

from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.lib.combo.TFA import check_2FA_lib
from src.lib.data_structure import dest_d
from src.lib.validators.idx import TFAFormT
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBodyReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.token import TokenT


async def recover_pwd_2FA_ctrl(
    req: Request,
    combo_res: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=False,
            model=TFAFormT,
            token_t=TokenT.RECOVER_PWD_2FA,
        )
    ),
) -> JSONResponse:
    async with db_trx() as trx:
        _, backup_codes_left = dest_d(
            await check_2FA_lib(trx, combo_res, delete_tok_on_check=False),
            ["user", "backup_codes_left"],
        )

        return ResAPI(req).ok_200(
            msg="verification successful", backup_codes_left=backup_codes_left
        )
