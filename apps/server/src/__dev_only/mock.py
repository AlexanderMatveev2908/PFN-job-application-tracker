import datetime
from typing import cast

from sqlalchemy import text
from src.__dev_only.payloads import gen_job_appl_payload
from src.conf.db import db_trx
from src.lib.counter import counter_cb
from src.lib.resdis.idx import clean_redis
from src.models.job_application import JobApplication
from src.models.root import RootTable
from src.models.user import User


async def reset_mock() -> None:
    async def cb() -> None:

        async with db_trx() as trx:

            for mp in RootTable.registry.mappers:
                await trx.execute(
                    text(f'TRUNCATE "{mp.class_.__tablename__}" CASCADE')
                )

            await clean_redis()

            us = {
                "first_name": "a",
                "last_name": "b",
                "email": "matveevalexander470@gmail.com",
                "is_verified": True,
                "password": "8cLS4XY!{2Wdvl4*l^4",
                "terms": True,
            }

            new_us_db = User(**us)
            trx.add(new_us_db)
            await trx.flush([new_us_db])
            await trx.refresh(new_us_db)

            for _ in range(10):
                payload = gen_job_appl_payload(new_us_db.id)

                dt = datetime.datetime.strptime(
                    cast(str, payload["applied_at"]), "%Y-%m-%d"
                ).replace(tzinfo=datetime.timezone.utc)

                payload["applied_at"] = int(dt.timestamp() * 1000)

                newJobAppl = JobApplication(**payload)
                trx.add(newJobAppl)
                await trx.flush([newJobAppl])
                await trx.refresh(newJobAppl)

    await counter_cb(cb)
