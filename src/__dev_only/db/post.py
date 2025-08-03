from sqlalchemy import select
from src.lib.logger import clg
from src.models.company import Company
from src.models.job import Job
from src.models.user import User
from ...conf.db import db_session


async def post_ud() -> None:
    async with db_session() as db:  # type: ignore
        try:
            await db.begin()

            us = User(
                first_name="John", last_name="Doe", email="john@gamil.com"
            )

            db.add(us)

            await db.flush([us])
            await db.refresh(us)

            print(us.to_d())

            await db.commit()

            clg(ttl="✅ 201")
        except Exception as err:
            clg(err, ttl="err transaction")

            await db.rollback()


async def post_c() -> None:
    async with db_session() as db:  # type: ignore
        try:
            await db.begin()

            c = Company(name="Burger King")

            db.add(c)

            await db.commit()
            clg(ttl="✅ op 200")
        except Exception as err:
            clg(err, ttl="💣 err transaction")
            await db.rollback()


async def post_j() -> None:
    async with db_session() as db:  # type: ignore
        try:
            await db.begin()

            us = await db.execute(
                select(User).where(User.first_name == "John")
            )
            c = await db.execute(
                select(Company).where(Company.name == "Burger King")
            )

            us_readable = us.scalars().one()
            c_readable = c.scalars().one()

            j = Job(
                title="Head Waiter",
                company_id=c_readable.id,
                user_id=us_readable.id,
            )

            db.add(j)

            await db.commit()
            clg(ttl="✅ op 200")
        except Exception as err:
            clg(err, ttl="💣 err transaction")
            await db.rollback()
