from logging.config import fileConfig
import os
from sqlalchemy import pool, create_engine
from alembic import context
from dotenv import load_dotenv
from src import models

target_metadata = models.Base.metadata


load_dotenv()
db_url = os.getenv("DB_URL")
if not db_url:
    raise RuntimeError("💣 missing db_url")


sync_db_url = db_url.replace("+asyncpg", "")

# Alembic config
config = context.config
config.set_main_option("sqlalchemy.url", sync_db_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = target_metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=sync_db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(sync_db_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
