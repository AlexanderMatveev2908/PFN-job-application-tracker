import math
import time
import uuid
from typing import Awaitable, Callable
from fastapi import Request, Response
from src.conf.redis import redis_session
from src.decorators.err import ErrAPI


def rate_limit(
    limit: int = 5, window_ms: int = 1000 * 60 * 15
) -> Callable[[Request, Response], Awaitable[None]]:
    async def _dep(req: Request, res: Response) -> None:
        async with redis_session() as r:
            ip = (
                (req.headers.get("x-forwarded-for", "")).split(",")[0]
                or getattr(req.client, "host", "")
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
                "RateLimit-Window": str(window_ms),
            }

            if count > limit:
                oldest_req = await r.execute_command(
                    "ZRANGE", k, 0, 0, "WITHSCORES"
                )

                if oldest_req:
                    oldest_ms = int(float(oldest_req[1]))
                    reset_s = max(
                        0, math.ceil((oldest_ms + window_ms - now) / 1000)
                    )
                else:
                    reset_s = int(window_ms / 1000)

                req.state.rate_limit_headers["RateLimit-Reset"] = str(reset_s)

                raise ErrAPI(
                    status=429,
                    msg="Our hamster-powered server took a break"
                    " — try again later! 🐹",
                )

    return _dep
