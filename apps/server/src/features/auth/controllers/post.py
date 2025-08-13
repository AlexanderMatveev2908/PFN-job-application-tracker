from fastapi import Depends, Request

from src.decorators.res import ResAPI
from src.features.auth.middleware.register import RegisterFormT, register_mdw


async def register_ctrl(
    _: Request, user_data: RegisterFormT = Depends(register_mdw)
) -> ResAPI:

    return ResAPI.ok_200(user_data=user_data)
