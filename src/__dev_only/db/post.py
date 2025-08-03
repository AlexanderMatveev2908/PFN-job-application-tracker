from sqlalchemy import select
from src.lib.logger import clg
from src.models.company import Company
from ...conf.db import db_session


async def add_data() -> None:
    async with db_session() as db:  # type: ignore
        try:
            await db.begin()

            res = await db.execute(
                select(Company).where(Company.name == "Taco Bell")  # type: ignore # noqa: E501
            )

            print(res)

            await db.commit()

            clg(ttl="✅ op 200")
        except Exception as err:
            clg(err, ttl="err transaction")

            await db.rollback()
