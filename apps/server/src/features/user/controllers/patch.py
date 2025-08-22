from fastapi import Depends, Request

from src.decorators.res import ResAPI
from src.features.user.middleware.action_account import ActionAccountMdwReturnT
from src.features.user.middleware.change_pwd import change_pwd_mdw


async def change_pwd_ctrl(
    req: Request,
    result_action_mdw: ActionAccountMdwReturnT = Depends(change_pwd_mdw),
) -> ResAPI:
    return ResAPI.ok_200(**result_action_mdw)
