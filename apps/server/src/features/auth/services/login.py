from typing import cast
from src.decorators.err import ErrAPI
from src.features.auth.middleware.login import LoginForm
from src.lib.db.idx import get_us_by_email
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


async def login_svc(login_data: LoginForm, trx: AsyncSession) -> User:

    us = cast(User, await get_us_by_email(trx, email=login_data.email))

    if not await us.check_pwd(login_data.password):
        raise ErrAPI(msg="invalid credentials", status=401)

    return us
