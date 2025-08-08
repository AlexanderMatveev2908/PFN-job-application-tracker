from typing import AsyncIterator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from src.conf.env import env_var
from contextlib import asynccontextmanager

from src.lib.logger import clg

engine = create_async_engine(
    env_var.db_url,
    echo=False,
)

db_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


@asynccontextmanager
async def db_trx() -> AsyncIterator[AsyncSession]:
    async with db_session() as db:
        try:
            await db.begin()

            yield db

            await db.commit()

            print("✅ trx 200")
        except Exception as err:
            await db.rollback()
            clg(err, ttl="err transaction")

            raise (err)
