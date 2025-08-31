from contextlib import asynccontextmanager
from typing import AsyncGenerator
from redis.asyncio import Redis

from src.conf.env import get_env

env_var = get_env()


@asynccontextmanager
async def redis_session() -> AsyncGenerator[Redis, None]:
    r = Redis.from_url(
        env_var.redis_url,
        encoding="utf-8",
        decode_responses=True,
        socket_timeout=5,
        socket_connect_timeout=5,
        health_check_interval=30,
    )

    try:
        yield r
    finally:
        try:
            await r.aclose()
        except Exception:
            await r.connection_pool.disconnect(inuse_connections=True)
