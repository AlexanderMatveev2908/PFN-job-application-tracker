from typing import cast
from fastapi import Request
from src.decorators.err import ErrAPI
from src.lib.validators.idx import PwdFormT
from src.middleware.forms.check_form import check_form_mdw
from src.middleware.tokens.check_jwt import check_jwt_search_us_mdw
from src.models.user import User, UserDcT


async def get_access_account_mdw(req: Request) -> UserDcT:
    us = cast(User, await check_jwt_search_us_mdw(inst=True)(req))

    result = await check_form_mdw(PwdFormT, req)

    if not await us.check_pwd(plain=result.password):
        raise ErrAPI(msg="invalid password", status=401)

    return cast(UserDcT, us.to_d())
