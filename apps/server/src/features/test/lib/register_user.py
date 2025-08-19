import uuid
from sqlalchemy import select
from src.features.auth.middleware.register import RegisterFormT
from src.lib.data_structure import parse_id
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def handle_user_lib(user_data: RegisterFormT, trx: AsyncSession) -> User:
    us = (
        await trx.execute(select(User).where(User.email == user_data["email"]))
    ).scalar_one_or_none()

    if not us:
        data = {k: v for k, v in user_data.items() if k != "password"}
        user_id = parse_id(uuid.uuid4())
        plain_pwd = user_data["password"]

        us = User(**data, id=user_id)
        await us.set_pwd(plain_pwd)
        trx.add(us)
        await trx.flush([us])
        await trx.refresh(us)

    return us
