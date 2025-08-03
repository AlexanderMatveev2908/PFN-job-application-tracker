from src.lib.logger import clg
from src.models.company import Company
from src.models.job import Job
from src.models.user import User
from ...conf.db import db_session


async def add_data() -> None:
    async with db_session() as db:  # type: ignore
        try:
            await db.begin()

            c = Company(name="Taco Bell")
            us = User(name="John", email="john@gmail.com")
            j = Job(title="Chef", company=c, user=us)

            db.add_all([c, us, j])

            await db.commit()

            clg(ttl="✅ op 200")
        except Exception as err:
            clg(err, ttl="err transaction")

            await db.rollback()
