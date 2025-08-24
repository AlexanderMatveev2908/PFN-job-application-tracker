from typing import cast
from fastapi import Request
from src.decorators.err import ErrAPI
from src.lib.validators.idx import PwdFormT
from src.middleware.check_form import check_form_mdw
from src.middleware.check_jwt import check_jwt_search_us_mdw
from src.models.user import User, UserDcT


async def manage_account_mdw(req: Request) -> UserDcT:
    us = cast(User, await check_jwt_search_us_mdw(req, inst=True))

    result = await check_form_mdw(PwdFormT, req)

    if not await us.check_pwd(plain=result.password):
        raise ErrAPI(msg="invalid password", status=401)

    return cast(UserDcT, us.to_d())
