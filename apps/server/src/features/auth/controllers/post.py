from fastapi import Depends, Request
from src.decorators.res import ResAPI
from src.features.auth.middleware.register import RegisterFormT, register_mdw
from src.features.auth.services.register_user import register_user_svc


async def register_ctrl(
    _: Request, user_data: RegisterFormT = Depends(register_mdw)
) -> ResAPI:

    result = await register_user_svc(user_data)

    return ResAPI.ok_200(
        new_user=result["new_user"],
        access_token=result["access_token"],
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
