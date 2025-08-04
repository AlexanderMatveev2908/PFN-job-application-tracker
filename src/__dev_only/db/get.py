import uuid
from sqlalchemy import select, text
from typing import Any
from sqlalchemy.orm import selectinload
from src.lib.logger import clg
from src.models.job import Job
from src.models.root import RootTable
from src.models.user import User
from ...conf.db import db_session


def raw_sql_where(**kwargs: Any) -> tuple[str, dict[str, Any]]:
    cond_parts: list[str] = []
    bind_params: dict[str, Any] = {}

    for k, v in kwargs.items():
        cond_parts.append(f"{k} = :{k}")
        bind_params[k] = v

    cond: str = "\nAND ".join(cond_parts)
    return cond, bind_params


async def run_raw_sql(
    txt: str,
    bind_params: dict[str, Any],
) -> list[dict[str, Any]]:
    async with db_session() as db:
        try:
            await db.begin()
            res = await db.execute(text(txt), bind_params)
            readable: list[dict[str, Any]] = [
                dict(r) for r in res.mappings().all()
            ]
            await db.commit()
            clg(ttl="✅ 200")
            return readable
        except Exception as err:
            clg(err, ttl="💣 err transaction")
            await db.rollback()
            return []


async def get_data_raw() -> None:

    cond, bind_params = raw_sql_where(
        name="John", email="john@gmail.com.changed"
    )

    txt = f"""
    SELECT * FROM users us
    WHERE {cond}
    """
    res = await run_raw_sql(txt, bind_params)

    print(res)


async def get_all() -> None:
    MODELS = {
        mapper.class_.__name__: mapper.class_
        for mapper in RootTable.registry.mappers
    }
    names = ["User", "Car", "Company", "Job"]

    async with db_session() as db:
        try:
            await db.begin()

            print("🤘🏼 data DB 🚀".center(16, " ").center(32, "―"))
            # print("\t")

            for k, v in MODELS.items():

                if k not in names:
                    continue

                res = await db.execute(select(v))
                rows = res.scalars().all()

                print(
                    f"🗃️ {k} — {len(rows)} 📦",
                )
                # print("—" * 50)
                # for r in rows:
                #     print(r.id)

                # print("\t")

            await db.commit()

        except Exception as err:
            clg(err, ttl="💣 err transaction")
            await db.rollback()


async def get_us_joined() -> None:
    async with db_session() as db:
        try:
            await db.begin()

            res = await db.execute(
                select(User)
                .where(
                    User.id
                    == uuid.UUID("bc984b98-b95b-45cb-83ef-871567e822d5")
                )
                .options(selectinload(User.jobs).joinedload(Job.company))
                # .options(selectinload(User.companies))
            )
            us = res.scalars().one()
            print(us.to_d(join=True, depth=2))

            await db.commit()
            print("✅ op 200")
        except Exception as err:
            clg(err, ttl="💣 err transaction")
            await db.rollback()
