from typing import Any
from redis.asyncio import Redis

from src.conf.env import get_env
from src.lib.logger import clg

env_var = get_env()

redis_db = Redis.from_url(
    env_var.redis_url,
    encoding="utf-8",
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5,
    health_check_interval=30,
)


async def check_redis() -> None:
    pong = await redis_db.ping()

    clg(pong, ttl="pong")


async def clean_redis() -> None:
    res = await redis_db.execute_command("FLUSHDB")

    print(res)


async def get_all_redis() -> None:

    rows: list[tuple[str, str, Any]] = []

    keys = await redis_db.execute_command("KEYS", "*") or {}

    for k in keys:

        t = await redis_db.execute_command("TYPE", k)

        if t == "string":
            v = await redis_db.execute_command("GET", k)
        elif t == "list":
            v = await redis_db.execute_command("LRANGE", k, 0, -1)
        elif t == " set":
            v = await redis_db.execute_command("SMEMBERS", k)
        elif t == "zset":
            v = await redis_db.execute_command(
                "ZRANGE",
                k,
                0,
                -1,
            )
        elif t == "hash":
            v = await redis_db.execute_command("HGETALL", k)
        elif t == "stream":
            v = await redis_db.execute_command(
                "XRANGE", k, "-", "+", "COUNT", 100
            )
        else:
            v = None

        rows.append((k, t or "unknown", v))

    if not rows:
        print("🗃️ redis is empty")

    for k, t, v in rows:
        print(f"🔑 {k} — 📊({t}) => {v}")
