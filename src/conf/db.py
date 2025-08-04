from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from src.conf.env import env_var


engine = create_async_engine(
    env_var.db_url,
    echo=False,
)
db_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def test_connect() -> None:

    async with db_session() as db:

        tables_result = await db.execute(
            text(
                """--sql
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """
            )
        )

        tables = [row[0] for row in tables_result]
        print(f"🗃️ DB TABLES => {(tables)}")
