from sqlalchemy import select
from src.lib.logger import clg
from src.models.user import User
from ...conf.db import db_session


async def patch_data() -> None:
    async with db_session() as db:
        try:
            await db.begin()
            c = (
                await db.execute(select(User).where(User.first_name == "John"))
            ).scalar()

            if c is None:
                return

            c.email = c.email + ".changed"

            print(c.to_d())

            await db.commit()
            clg(ttl="✅ op 200")
        except Exception as err:
            clg(err, ttl="💣 err transaction")
            await db.rollback()
