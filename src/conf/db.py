from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.conf.env import env_var


engine = create_async_engine(
    env_var.db_url,
    echo=False,
)
db_session = sessionmaker(  # type: ignore
    bind=engine, expire_on_commit=False, class_=AsyncSession  # type: ignore
)


async def test_connect() -> None:

    async with db_session() as db:  # type: ignore

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
