from fastapi import Request

from src.features.user.middleware.action_account import (
    ActionAccountMdwReturnT,
    action_account_mdw,
)
from src.lib.validators.idx import PwdFormT
from src.middleware.check_form import check_form_mdw
from src.middleware.check_jwt import check_jwt_mdw


async def change_pwd_mdw(req: Request) -> ActionAccountMdwReturnT:
    check_jwt_mdw(req)

    result_action_mdw: ActionAccountMdwReturnT = await action_account_mdw(req)

    await check_form_mdw(model=PwdFormT, data=result_action_mdw["body"])

    return result_action_mdw
