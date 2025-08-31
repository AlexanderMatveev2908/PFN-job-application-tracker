from typing import Any
from src.conf.redis import redis_session
from src.lib.logger import clg


async def check_redis() -> None:
    async with redis_session() as r:
        pong = await r.ping()

    clg(pong, ttl="pong")


async def clean_redis() -> None:
    async with redis_session() as r:
        await r.execute_command("FLUSHDB")

        print("🔪 cleaned redis")


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
