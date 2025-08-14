from sqlalchemy import text
from src.conf.db import db_trx
from src.models.root import RootTable


async def clean_tables() -> None:
    async with db_trx() as trx:
        for mp in RootTable.registry.mappers:
            await trx.execute(
                text(f'TRUNCATE "{mp.class_.__tablename__}" CASCADE')
            )
