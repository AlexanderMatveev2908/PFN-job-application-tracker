from typing import Any
from sqlalchemy import text
from src.lib.logger import clg
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

    txt = f"""--sql
    SELECT * FROM users us
    WHERE {cond}
    """

    res = await run_raw_sql(txt, bind_params)

    print(res)
