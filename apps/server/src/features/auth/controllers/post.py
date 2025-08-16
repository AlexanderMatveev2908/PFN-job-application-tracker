from typing import cast
from fastapi import Depends, Request
from src.decorators.res import ResAPI
from src.features.auth.middleware.register import RegisterFormT, register_mdw
from src.features.auth.services.register_user import register_user_svc
from src.lib.data_structure import pick


async def register_ctrl(
    _: Request, user_data: RegisterFormT = Depends(register_mdw)
) -> ResAPI:

    result = await register_user_svc(user_data)

    return ResAPI.ok_200(
        **pick(obj=cast(dict, result), keys_off=["refresh_token"]),
        cookies=[
            {
                "key": "refresh_token",
                "value": result["refresh_token"],
                "httponly": True,
                "secure": True,
                "samesite": "none",
                "max_age": 60**2 * 24,
                "path": "/",
            },
        ],
    )
