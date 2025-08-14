from redis.asyncio import Redis

from src.conf.env import get_env
from src.lib.logger import clg

env_var = get_env()

redis = Redis.from_url(
    env_var.redis_url,
    encoding="utf-8",
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5,
    health_check_interval=30,
)


async def check_redis() -> None:
    pong = await redis.ping()

    clg(pong, ttl="pong")
