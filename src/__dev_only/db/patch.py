from sqlalchemy import select
from src.lib.logger import clg
from src.models.user import User
from ...conf.db import db_session


async def patch_data() -> None:
    async with db_session() as db:  # type: ignore
        try:
            await db.begin()
            c = (
                await db.execute(select(User).where(User.name == "John"))
            ).scalar()
            c.email = c.email + ".changed"

            print(c.to_d())

            await db.commit()
            clg(ttl="✅ op 200")
        except Exception as err:
            clg(err, ttl="💣 err transaction")
            await db.rollback()
