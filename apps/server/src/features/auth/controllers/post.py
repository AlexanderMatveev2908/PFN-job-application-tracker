from typing import cast
from fastapi import Depends, Request
from src.decorators.res import ResAPI
from src.features.auth.middleware.register import RegisterFormT, register_mdw
from src.features.auth.services.register_user import register_user_svc
from src.lib.cookies import gen_refresh_cookie
from src.lib.data_structure import pick


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


async def login_ctrl(req: Request) -> ResAPI:
    return ResAPI.ok_200()
