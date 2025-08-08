from uuid import UUID
from fastapi import Depends, Request

from src.decorators.res import ResAPI
from src.features.test.services.get_user import get_user_svc
from src.middleware.check_id import check_id_mdw


async def get_msg_ctrl(_: Request) -> ResAPI:

    return ResAPI.ok_200(msg="✅ get request ☎️")


async def get_user_ctrl(
    _: Request, id: UUID = Depends(check_id_mdw("user_id"))
) -> ResAPI:

    us = await get_user_svc(id)

    return ResAPI.ok_200(us=us.to_d(joins=True, max_depth=2))
