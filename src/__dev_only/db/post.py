from src.lib.logger import clg
from src.models.user import User
from ...conf.db import db_session


async def add_data_ud() -> None:
    async with db_session() as db:  # type: ignore
        try:
            await db.begin()

            us = User(
                first_name="Mike", last_name="Doe", email="mike@gamil.com"
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
