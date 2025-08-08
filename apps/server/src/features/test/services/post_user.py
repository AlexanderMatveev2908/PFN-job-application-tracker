from src.conf.db import db_trx
from src.features.test.middleware.check_user import UserT
from src.models.user import User


async def post_user_svc(user: UserT) -> User:

    async with db_trx() as trx:
        us = User(
            **user.model_dump(
                by_alias=False, exclude_none=True, exclude_unset=True
            )
        )
        trx.add(us)
        await trx.flush([us])
        await trx.refresh(us)

        return us
