import time
from typing import Awaitable, Callable
import uuid
from fastapi import Request
from src.conf.redis import redis_db
from src.decorators.err import ErrAPI


def rate_limit(
    limit: int = 5, window_ms: float = 900000
) -> Callable[[Request], Awaitable[None]]:
    async def _dep(req: Request) -> None:
        ip = (
            (req.headers.get("x-forwarded-for", "")).split(",")[0]
            or (getattr(req.client, "host", ""))
        ).strip() or "unknown"

        now = int(time.time() * 1000)

        k = f"rl:{ip}:{req.url.path}"
        v = f"{now}:{uuid.uuid4()}"

        await redis_db.execute_command(
            "ZREMRANGEBYSCORE", k, 0, now - window_ms
        )

        await redis_db.execute_command("ZADD", k, now, v)

        count = await redis_db.execute_command("ZCARD", k) or 0

        await redis_db.execute_command(
            "EXPIRE", k, int((window_ms / 1000) + 1)
        )

        opt = {
            "X-RateLimit-Limit": str(limit),
            "X-RateLimit-Remaining": str(max(0, limit - count)),
            "X-RateLimit-Window": str(int(window_ms)),
        }

        req.state.rate_limit_headers = {**opt}

        if (count or 0) > limit:
            raise ErrAPI(
                status=429,
                msg="Our hamster-powered server took a break"
                " — try again later! 🐹",
                opt=opt,
            )

    return _dep
