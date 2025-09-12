from typing import TypedDict, cast
from fastapi import Request

from src.constants.reg import REG_ID
from src.decorators.err import ErrAPI
from src.middleware.tokens.check_jwt import check_jwt_search_us_mdw
from src.models.user import UserDcT


class GetApplByIdMdwReturnT(TypedDict):
    us_d: UserDcT
    application_id: str


async def get_appl_by_id_mdw(req: Request) -> GetApplByIdMdwReturnT:
    application_id = req.path_params.get("application_id", "")

    if not REG_ID.fullmatch(application_id):
        raise ErrAPI(msg="invalid application id", status=422)

    us_d: UserDcT = cast(UserDcT, await check_jwt_search_us_mdw()(req))

    return {"us_d": us_d, "application_id": application_id}
