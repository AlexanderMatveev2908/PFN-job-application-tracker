from contextlib import asynccontextmanager
import datetime
from typing import AsyncGenerator, Awaitable, Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sqlalchemy import delete

from src.conf.db import db_trx
from src.lib.etc import get_now
from src.models.token import Token


async def clear_exp_tokens() -> None:
    async with db_trx() as trx:
        stmt = delete(Token).where(Token.exp < get_now())
        await trx.execute(stmt)


@asynccontextmanager
async def scheduler_ctx(
    cb: Callable[[], Awaitable[None]],
    *,
    job_id: str,
    hours: int = 24,
) -> AsyncGenerator[None, None]:
    sched = AsyncIOScheduler()
    sched.add_job(
        cb,
        trigger="interval",
        hours=hours,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=300,
        next_run_time=datetime.datetime.now(datetime.timezone.utc),
        id=job_id,
        replace_existing=True,
    )

    sched.start()

    try:
        yield
    finally:
        sched.shutdown(wait=False)
