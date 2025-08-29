from fastapi import Depends, Request
from fastapi.responses import JSONResponse

from src.decorators.res import ResAPI
from src.lib.data_structure import pick
from src.middleware.check_jwt import check_jwt_search_us_mdw
from src.models.user import UserDcT


async def get_us_profile_ctrl(
    req: Request, us: UserDcT = Depends(check_jwt_search_us_mdw)
) -> JSONResponse:

    filtered = pick(us, keys_off=["password", "totp_secret"])

    return ResAPI(req).ok_200(user=filtered)
