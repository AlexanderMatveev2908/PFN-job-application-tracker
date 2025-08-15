import time
from typing import Awaitable, Callable
import uuid
from fastapi import Request, Response
from src.conf.redis import redis_session
from src.decorators.err import ErrAPI


def rate_limit(
    limit: int = 5, window_ms: float = 1000 * 60 * 15
) -> Callable[[Request, Response], Awaitable[None]]:
    async def _dep(req: Request, res: Response) -> None:

        async with redis_session() as r:

            ip = (
                (req.headers.get("x-forwarded-for", "")).split(",")[0]
                or (getattr(req.client, "host", ""))
            ).strip() or "unknown"

            now = int(time.time() * 1000)

            k = f"rl:{ip}:{req.url.path}"
            v = f"{now}:{uuid.uuid4()}"

            await r.execute_command("ZREMRANGEBYSCORE", k, 0, now - window_ms)

            await r.execute_command("ZADD", k, now, v)

            count = await r.execute_command("ZCARD", k) or 0

            await r.execute_command("EXPIRE", k, int((window_ms / 1000) + 1))

            remaining = max(0, limit - count)

            req.state.rate_limit_headers = {
                "RateLimit-Limit": str(limit),
                "RateLimit-Remaining": str(remaining),
                "RateLimit-Window": str(int(window_ms)),
            }

            if (count or 0) > limit:
                raise ErrAPI(
                    status=429,
                    msg="Our hamster-powered server took a break"
                    " — try again later! 🐹",
                )

    return _dep
