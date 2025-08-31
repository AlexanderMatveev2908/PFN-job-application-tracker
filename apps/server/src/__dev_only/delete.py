from sqlalchemy import text
from src.conf.db import db_trx
from src.lib.counter import counter_cb
from src.lib.resdis.idx import clean_redis
from src.models.root import RootTable


async def clean_DBs(del_redis: bool = False) -> None:

    async def cb() -> None:
        async with db_trx() as trx:
            for mp in RootTable.registry.mappers:
                await trx.execute(
                    text(f'TRUNCATE "{mp.class_.__tablename__}" CASCADE')
                )

        if del_redis:
            await clean_redis()

    await counter_cb(cb)
