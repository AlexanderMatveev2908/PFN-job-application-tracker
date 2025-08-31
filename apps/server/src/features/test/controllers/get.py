from fastapi import Depends, Request
from fastapi.responses import Response
from src.decorators.res import ResAPI
from src.middleware.tokens.check_jwt import check_jwt_search_us_mdw
from src.models.user import UserDcT


async def get_msg_ctrl(req: Request) -> Response:

    return ResAPI(req).ok_200(
        msg="✅ get request ☎️",
    )


async def get_protected_data_ctrl(
    req: Request, us: UserDcT = Depends(check_jwt_search_us_mdw())
) -> Response:
    return ResAPI(req).ok_200(msg="protected data 👻", us=us)
