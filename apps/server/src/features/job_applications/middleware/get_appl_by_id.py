from typing import cast
from fastapi import Request

from src.lib.validators.idx import check_id_lib
from src.middleware.tokens.check_jwt import check_jwt_search_us_mdw
from src.models.user import UserDcT
from src.my_types.idx import UserDctReturnT


class GetApplByIdMdwReturnT(UserDctReturnT):
    application_id: str


async def get_appl_by_id_mdw(req: Request) -> GetApplByIdMdwReturnT:
    application_id = check_id_lib(req, "application_id")

    us_d: UserDcT = cast(UserDcT, await check_jwt_search_us_mdw()(req))

    return {"us_d": us_d, "application_id": application_id}
