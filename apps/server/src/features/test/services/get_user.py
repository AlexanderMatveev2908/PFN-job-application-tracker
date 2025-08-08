from uuid import UUID
from sqlalchemy import select
from src.conf.db import db_trx
from src.models.job import Job
from src.models.user import User
from sqlalchemy.orm import selectinload, joinedload


async def get_user_svc(id: UUID) -> User:

    async with db_trx() as trx:

        stmt = (
            select(User)
            .where(User.id == id)
            .options(
                selectinload(User.jobs).options(joinedload(Job.company)),
                selectinload(User.cars),
            )
        )

        res = await trx.execute(stmt)
        us: User = res.scalars().one()

        return us
