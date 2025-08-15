from fastapi import Depends, Request

from src.decorators.res import ResAPI
from src.features.auth.middleware.register import RegisterFormT, register_mdw
from src.features.auth.services.register_user import register_user_svc
from src.lib.tokens.jwt import gen_jwt


async def register_ctrl(
    _: Request, user_data: RegisterFormT = Depends(register_mdw)
) -> ResAPI:

    new_user = await register_user_svc(user_data)

    access_token = gen_jwt(id=str(new_user.id))

    return ResAPI.ok_200(
        new_user=new_user.to_d(exclude_keys=["password"]),
        access_token=access_token,
    )
