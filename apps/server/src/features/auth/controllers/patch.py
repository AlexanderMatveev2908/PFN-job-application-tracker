from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from src.decorators.err import ErrAPI
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
    req: Request,
    result_combo: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            model=PwdFormT, token_t=TokenT.RECOVER_PWD, check_jwt=False
        )
    ),
) -> JSONResponse:

    if result_combo["cbc_hmac_result"]["user_d"]["totp_secret"]:
        raise ErrAPI(msg="user must follow 2fa flow", status=403)

    result_tokens = await change_pwd_svc(result_combo)

    return ResAPI(
        req,
        cookies=[
            gen_refresh_cookie(result_tokens["result_jwe"]["client_token"])
        ],
    ).ok_200(
        msg="password updated",
        access_token=result_tokens["access_token"],
    )


async def revocer_pwd_2FA_ctrl(
    req: Request,
    result_combo: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            model=PwdFormT, token_t=TokenT.RECOVER_PWD_2FA, check_jwt=False
        )
    ),
) -> JSONResponse:

    result_tokens = await change_pwd_svc(result_combo)

    return ResAPI(
        req,
        cookies=[
            gen_refresh_cookie(result_tokens["result_jwe"]["client_token"])
        ],
    ).ok_200(
        msg="password updated",
        access_token=result_tokens["access_token"],
    )
