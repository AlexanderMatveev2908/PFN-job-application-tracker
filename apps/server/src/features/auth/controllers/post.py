from typing import cast
from fastapi import Depends, Request
from src.decorators.res import ResAPI
from src.features.auth.middleware.login import LoginForm, login_mdw
from src.features.auth.middleware.recover_pwd import (
    RecoverPwdMdwReturnT,
    recover_pwd_mdw,
)
from src.features.auth.middleware.register import RegisterFormT, register_mdw
from src.features.auth.services.change_pwd import change_pwd_svc
from src.features.auth.services.login import login_svc
from src.features.auth.services.register import register_user_svc
from src.lib.cookies import gen_refresh_cookie
from src.lib.data_structure import pick
from src.lib.tokens.combo import TokensSessionsReturnT


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
    data_recover_pwd: RecoverPwdMdwReturnT = Depends(recover_pwd_mdw),
) -> ResAPI:

    access_token, refresh_result = await change_pwd_svc(data_recover_pwd)

    return ResAPI.ok_200(
        msg="password updated",
        access_token=access_token,
        cookies=[gen_refresh_cookie(refresh_result["client_token"])],
    )


async def refresh_token_ctrl(req: Request) -> ResAPI:
    return ResAPI.ok_200()
