from sqlalchemy import select
from typing import Any
from src.models.root import RootTable
from ...conf.db import db_trx


def raw_sql_where(**kwargs: Any) -> tuple[str, dict[str, Any]]:
    cond_parts: list[str] = []
    bind_params: dict[str, Any] = {}

    for k, v in kwargs.items():
        cond_parts.append(f"{k} = :{k}")
        bind_params[k] = v

    cond: str = "\nAND ".join(cond_parts)
    return cond, bind_params


async def get_all() -> None:
    MODELS = {
        mapper.class_.__name__: mapper.class_
        for mapper in RootTable.registry.mappers
    }
    names = ["User", "Car", "Company", "Job"]

    async with db_trx() as trx:
        print("🤘🏼 data DB 🚀".center(16, " ").center(32, "―"))

        for k, v in MODELS.items():

            if k not in names:
                continue

            res = await trx.execute(select(v))
            rows = res.scalars().all()

            print(
                f"🗃️ {k} — {len(rows)} 📦",
            )
