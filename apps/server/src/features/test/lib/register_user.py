import uuid
from sqlalchemy import text
from src.decorators.err import ErrAPI
from src.features.auth.middleware.register import RegisterFormT
from src.lib.data_structure import parse_id
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def handle_user_lib(user_data: RegisterFormT, trx: AsyncSession) -> User:
    stm = """
        SELECT us.*
        FROM users us
        WHERE us.email = :email
        LIMIT 1
        """
    row = (await trx.execute(text(stm), {"email": user_data["email"]})).first()

    if row:
        us = await trx.get(User, row.id)
    else:
        data = {k: v for k, v in user_data.items() if k != "password"}
        user_id = parse_id(uuid.uuid4())
        plain_pwd = user_data["password"]

        us = User(**data, id=user_id)
        await us.set_pwd(plain_pwd)
        trx.add(us)
        await trx.flush([us])
        await trx.refresh(us)

    if not us:
        raise ErrAPI(msg="👻 user disappeared", status=500)

    return us
