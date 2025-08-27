from fastapi import Depends, Request

from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.auth.middleware.login_backup_code import BackupCodeFormT
from src.features.auth.middleware.login_totp import TotpFormT
from src.lib.db.idx import get_us_by_id
from src.lib.etc import grab
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBodyReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.token import TokenT


async def forgot_pwd_2FA_totp_ctrl(
    req: Request,
    combo_res: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=False, model=TotpFormT, token_t=TokenT.RECOVER_PWD_2FA
        )
    ),
) -> ResAPI:

    async with db_trx() as trx:
        us = await get_us_by_id(trx, grab(combo_res, "user_id"))

        if not us.check_totp(grab(combo_res, "totp_code", parent="body")):
            raise ErrAPI(msg="totp_code_invalid", status=401)

        return ResAPI.ok_200(msg="verification successful")


async def forgot_pwd_2FA_backup_code_ctrl(
    req: Request,
    res_combo: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=False,
            model=BackupCodeFormT,
            token_t=TokenT.RECOVER_PWD_2FA,
        )
    ),
) -> ResAPI:

    async with db_trx() as trx:
        us = await get_us_by_id(trx, grab(res_combo, "user_id"))

        backup_code = await us.check_backup_code(
            trx, grab(res_combo, "backup_code")
        )

        return ResAPI.ok_200(
            msg="verification successful",
            backup_codes_left=backup_code["backup_codes_left"],
        )
