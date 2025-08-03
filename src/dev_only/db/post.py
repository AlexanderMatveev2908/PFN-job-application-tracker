from sqlalchemy import select
from src.decorators.err import ErrGen
from src.lib.logger import clg
from src.models.company import Company
from src.models.job import Job
from src.models.user import User
from ...conf.db import db_session


async def add_data() -> None:
    async with db_session() as db:  # type: ignore
        try:
            await db.begin()

            res = await db.execute(
                select(Company).where(Company.name == "Taco Bell")
            )
            c = res.scalar_one_or_none()

            if not c:
                raise ErrGen("No company found")

            us = User(name="Jane", email="jane@gmail.com")
            j = Job(title="Head Waiter", company=c, user=us)

            db.add_all([c, us, j])

            await db.commit()

            clg(ttl="✅ op 200")
        except Exception as err:
            clg(err, ttl="err transaction")

            await db.rollback()
