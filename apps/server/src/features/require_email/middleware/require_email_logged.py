from typing import cast
from fastapi import Request

from src.decorators.err import ErrAPI
from src.features.require_email.middleware.require_email import (
    RequireEmailForm,
)
from src.middleware.forms.check_form import check_form_mdw
from src.middleware.tokens.check_jwt import check_jwt_search_us_mdw
from src.models.user import User, UserDcT


async def require_email_logged_mdw(req: Request) -> UserDcT:
    us = cast(User, await check_jwt_search_us_mdw(inst=True)(req))

    data = await check_form_mdw(RequireEmailForm, req)

    if us.is_verified:
        raise ErrAPI(msg="user already verified", status=409)

    if us.email != data.email:
        raise ErrAPI(
            msg="email different from one declared at register time",
            status=400,
        )

    return cast(UserDcT, us.to_d())
