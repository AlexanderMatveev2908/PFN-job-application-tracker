from typing import cast
from fastapi import Request
from sqlalchemy import select
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.validators.idx import EmailForm
from src.middleware.check_form import check_form_mdw
from src.models.user import User, UserDcT


class RequireEmailForm(EmailForm):
    pass


async def require_email_mdw(req: Request) -> UserDcT:
    data = await check_form_mdw(RequireEmailForm, req)

    async with db_trx() as trx:
        us = (
            await trx.execute(select(User).where(User.email == data.email))
        ).scalar_one_or_none()

        if not us:
            raise ErrAPI(msg="user not found", status=404)

    return cast(UserDcT, us.to_d())
