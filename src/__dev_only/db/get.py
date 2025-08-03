from sqlalchemy import select
from typing import Any
from sqlalchemy import text
from src.lib.logger import clg
from src.models.root import RootTable
from ...conf.db import db_session


def raw_sql_where(**kwargs) -> tuple[str, dict[str, Any]]:
    cond = []
    bind_params = {}

    for k, v in kwargs.items():
        cond.append(f"{k} = :{k}")
        bind_params[k] = v

    cond = "\nAND ".join(cond)

    return cond, bind_params


async def run_raw_sql(
    txt: str,
    bind_params: dict,
) -> list[dict]:

    async with db_session() as db:  # type: ignore
        try:
            await db.begin()

            res = await db.execute(text(txt), bind_params)
            readable = [dict(r) for r in res.mappings().all()]

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

    async with db_session() as db:  # type: ignore
        try:
            await db.begin()

            print("🤘🏼 data DB 🚀".center(16, " ").center(40, "―"))
            print("\t")

            for k, v in MODELS.items():

                if k not in names:
                    continue

                res = await db.execute(select(v))
                rows = res.scalars().all()

                print(
                    f"🗃️ {k} 📦",
                )
                print("—" * 50)
                for r in rows:
                    print(r.to_d())
                    print("\t")

                print("\t")

            await db.commit()

        except Exception as err:
            clg(err, ttl="💣 err transaction")
            await db.rollback()
