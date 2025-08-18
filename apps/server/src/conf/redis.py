from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from redis.asyncio import Redis

from src.conf.env import get_env
from src.lib.logger import clg

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


async def check_redis() -> None:
    async with redis_session() as r:
        pong = await r.ping()

    clg(pong, ttl="pong")


async def clean_redis() -> None:
    async with redis_session() as r:
        await r.execute_command("FLUSHDB")

    print("✅ redis 200")


async def get_all_redis() -> None:
    async with redis_session() as r:

        rows: list[tuple[str, str, Any]] = []

        keys = await r.execute_command("KEYS", "*") or {}

        for k in keys:

            t = await r.execute_command("TYPE", k)

            if t == "string":
                v = await r.execute_command("GET", k)
            elif t == "list":
                v = await r.execute_command("LRANGE", k, 0, -1)
            elif t == " set":
                v = await r.execute_command("SMEMBERS", k)
            elif t == "zset":
                v = await r.execute_command(
                    "ZRANGE",
                    k,
                    0,
                    -1,
                )
            elif t == "hash":
                v = await r.execute_command("HGETALL", k)
            elif t == "stream":
                v = await r.execute_command(
                    "XRANGE", k, "-", "+", "COUNT", 100
                )
            else:
                v = None

            rows.append((k, t or "unknown", v))

        if not rows:
            print("🗃️ redis is empty")

        for k, t, v in rows:
            print(f"🔑 {k} — 📊({t}) => {v}")
