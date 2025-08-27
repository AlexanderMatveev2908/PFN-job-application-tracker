from fastapi import Depends, Request

from src.decorators.res import ResAPI
from src.features.auth.middleware.login_totp import TotpFormT
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

    return ResAPI.ok_200(msg="verification successful")
