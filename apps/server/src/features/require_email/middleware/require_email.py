from typing import cast
from fastapi import Request
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.db.idx import get_us_by_email
from src.lib.validators.idx import EmailFormT
from src.middleware.forms.check_form import check_form_mdw
from src.models.user import User, UserDcT


class RequireEmailForm(EmailFormT):
    pass


async def require_email_mdw(req: Request) -> UserDcT:
    data = await check_form_mdw(RequireEmailForm, req)

    async with db_trx() as trx:
        us = cast(User, await get_us_by_email(trx, data.email))

        if us.is_verified:
            raise ErrAPI(msg="user already verified", status=409)

    return cast(UserDcT, us.to_d())
