from fastapi import Depends, Request
from src.decorators.res import ResAPI
from src.features.auth.services.change_pwd import change_pwd_svc
from src.lib.cookies import gen_refresh_cookie
from src.lib.validators.idx import PwdFormT
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBodyReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.token import TokenT


async def recover_pwd_ctrl(
    _: Request,
    result_combo: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            model=PwdFormT, token_t=TokenT.RECOVER_PWD, check_jwt=False
        )
    ),
) -> ResAPI:

    result_tokens = await change_pwd_svc(result_combo)

    return ResAPI.ok_200(
        msg="password updated",
        access_token=result_tokens["access_token"],
        cookies=[
            gen_refresh_cookie(result_tokens["result_jwe"]["client_token"])
        ],
    )
