from fastapi import Depends, Request
from src.decorators.res import ResAPI
from src.middleware.check_jwt import CheckJwtMdwReturnT, check_check_jwt_mdw


async def get_msg_ctrl(req: Request) -> ResAPI:

    return ResAPI.ok_200(
        msg="✅ get request ☎️",
    )


async def get_protected_data_ctrl(
    req: Request, us_data: CheckJwtMdwReturnT = Depends(check_check_jwt_mdw)
) -> ResAPI:
    return ResAPI.ok_200(**us_data)
