from typing import cast
from fastapi import Depends, Request
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.auth.middleware.login import LoginForm, login_mdw
from src.features.auth.middleware.register import RegisterFormT, register_mdw
from src.features.auth.services.change_pwd import change_pwd_svc
from src.features.auth.services.login import login_svc
from src.features.auth.services.register import register_user_svc
from src.lib.cookies import gen_refresh_cookie
from src.lib.data_structure import pick
from src.lib.tokens.combo import TokensSessionsReturnT
from src.lib.tokens.jwe import check_jwe
from src.lib.tokens.jwt import gen_jwt
from src.lib.validators.idx import PwdFormT
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBdReturnT,
    combo_check_bd_jwt_bcb_hmac_mdw,
)
from src.models.token import CheckTokenReturnT, TokenT


async def register_ctrl(
    _: Request, user_data: RegisterFormT = Depends(register_mdw)
) -> ResAPI:

    result = await register_user_svc(user_data)

    return ResAPI.ok_201(
        **pick(obj=cast(dict, result), keys_off=["refresh_token"]),
        cookies=[
            gen_refresh_cookie(result["refresh_token"]),
        ],
    )


async def login_ctrl(
    _: Request, login_data: LoginForm = Depends(login_mdw)
) -> ResAPI:

    access_token, jwe_result = cast(
        TokensSessionsReturnT, await login_svc(login_data)
    )

    return ResAPI.ok_200(
        access_token=access_token,
        cookies=[gen_refresh_cookie(jwe_result["client_token"])],
    )


async def recover_pwd_ctrl(
    _: Request,
    result_combo: ComboCheckJwtCbcBdReturnT = Depends(
        combo_check_bd_jwt_bcb_hmac_mdw(
            model=PwdFormT, token_t=TokenT.RECOVER_PWD, check_jwt=False
        )
    ),
) -> ResAPI:

    access_token, refresh_result = await change_pwd_svc(result_combo)

    return ResAPI.ok_200(
        msg="password updated",
        access_token=access_token,
        cookies=[gen_refresh_cookie(refresh_result["client_token"])],
    )


async def refresh_token_ctrl(req: Request) -> ResAPI:
    refresh = req.cookies.get("refresh_token")

    if not refresh:
        raise ErrAPI(msg="REFRESH_TOKEN_NOT_PROVIDED", status=401)

    async with db_trx() as trx:
        try:
            result_jwe: CheckTokenReturnT = await check_jwe(
                token=refresh, trx=trx
            )
            access_token = gen_jwt(user_id=result_jwe["user_d"]["id"])

            return ResAPI.ok_200(access_token=access_token)
        except Exception as err:
            msg = err.msg if isinstance(err, ErrAPI) else str(err)

            return ResAPI.err_401(msg=msg, clear_cookies=["refresh_token"])
