import binascii
import ssl
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


ca_pem = binascii.unhexlify(env_var.supabase_ca).decode("utf-8")
ssl_ctx = ssl.create_default_context()
ssl_ctx.load_verify_locations(cadata=ca_pem)

engine = create_async_engine(
    cast(str, env_var.db_url),
    echo=False,
    pool_pre_ping=True,
    poolclass=(NullPool if env_var.next_public_front_url_test else None),
    connect_args={"ssl": ssl_ctx},
)

db_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
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
