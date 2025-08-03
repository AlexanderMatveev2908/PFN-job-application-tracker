from sqlalchemy import select
from src.lib.logger import clg
from src.models.company import Company
from src.models.user import User
from ...conf.db import db_session


async def add_data() -> None:
    async with db_session() as db:  # type: ignore
        try:
            await db.begin()

            res = (
                (
                    await db.execute(
                        select(Company).where(Company.name == "Taco Bell")  # type: ignore # noqa: E501
                    )
                )
            ).all()

            us = User(first_name="John")

            # c = Company(
            #     name="Burger King",
            # )
            # db.add(c)
            # await db.flush([c])

            await db.commit()

        except Exception as err:
            clg(err, ttl="err transaction")

            await db.rollback()
