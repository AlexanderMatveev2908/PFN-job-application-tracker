from fastapi import Depends, Request
from fastapi.responses import Response

from src.decorators.res import ResAPI
from src.lib.data_structure import pick
from src.middleware.tokens.check_jwt import check_jwt_search_us_mdw
from src.models.user import User, UserDcT


async def get_us_profile_ctrl(
    req: Request,
    us: User | UserDcT | None = Depends(
        check_jwt_search_us_mdw(optional=True)
    ),
) -> Response:

    if not us:
        return ResAPI(req).ok_204()

    filtered = pick(us, keys_off=["password", "totp_secret"])

    return ResAPI(req).ok_200(user=filtered)
