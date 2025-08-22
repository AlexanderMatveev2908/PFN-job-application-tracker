from fastapi import Depends, Request
from src.decorators.res import ResAPI
from src.middleware.check_jwt import check_jwt_search_us_mdw
from src.models.user import UserDcT


async def get_msg_ctrl(req: Request) -> ResAPI:

    return ResAPI.ok_200(
        msg="✅ get request ☎️",
    )


async def get_protected_data_ctrl(
    _: Request, us: UserDcT = Depends(check_jwt_search_us_mdw)
) -> ResAPI:
    return ResAPI.ok_200(msg="protected data 👻")
