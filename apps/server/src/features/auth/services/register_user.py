from sqlalchemy import select
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.features.auth.middleware.register import RegisterFormT
from src.models.user import User


async def register_user_svc(user_data: RegisterFormT) -> User:
    async with db_trx() as trx:

        stmt = select(User).where(User.email == user_data["email"])
        existing = (await trx.execute(stmt)).scalar_one_or_none()

        if existing:
            raise ErrAPI(msg="user already exists", status=409)

        data = {k: v for k, v in user_data.items() if k != "password"}
        plain_pwd = user_data["password"]
        new_user = User(**data)
        await new_user.set_pwd(plain_pwd)

        trx.add(new_user)
        await trx.flush([new_user])
        await trx.refresh(new_user)

        return new_user
