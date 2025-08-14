from typing import AsyncIterator, cast
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from src.conf.env import get_env
from contextlib import asynccontextmanager
from src.lib.logger import clg

env_var = get_env()

engine = create_async_engine(
    cast(str, env_var.db_url),
    echo=False,
    pool_pre_ping=True,
    poolclass=(NullPool if env_var.next_public_front_url_test else None),
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
