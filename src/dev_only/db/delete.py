from sqlalchemy import delete, select

from src.lib.logger import clg
from src.models.job import Job
from src.models.user import User
from ...conf.db import db_session


async def del_row() -> None:
    async with db_session() as db:  # type: ignore
        try:
            await db.begin()

            c = (
                await db.execute(select(User).where(User.name == "Jane"))
            ).scalar()

            if c:
                res_jobs = (
                    await db.execute(delete(Job).where(Job.user_id == c.id))
                ).rowcount
                await db.delete(c)

                print(f"🔪 deleted {res_jobs} jobs")

            else:
                print("user not found")

            # print(c.to_d())

            await db.commit()
            clg(ttl="✅ op 200")
        except Exception as err:
            clg(err, ttl="💣 err transaction")
            await db.rollback()
