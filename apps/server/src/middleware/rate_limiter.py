import math
import uuid
from typing import Awaitable, Callable, cast
from fastapi import Request, Response
from src.conf.env import get_env
from src.conf.redis import redis_session
from src.constants.api import EXPOSE_HEADERS
from src.decorators.err import ErrAPI
from src.lib.etc import get_now
from src.my_types.idx import MAPPER_WINDOW_TIME, ParamWindowTime


def merge_exp_hdr(base: dict[str, str]) -> dict[str, str]:

    merged = {**base}
    expose_vals = ", ".join(EXPOSE_HEADERS)

    if "Access-Control-Expose-Headers" in merged:
        existing = set(
            map(str.strip, merged["Access-Control-Expose-Headers"].split(","))
        )
        merged["Access-Control-Expose-Headers"] = ", ".join(
            sorted(existing.union(EXPOSE_HEADERS))
        )
    else:
        merged["Access-Control-Expose-Headers"] = expose_vals

    return merged


def rate_limit_mdw(
    limit: int = 5, window_arg: ParamWindowTime = "30m"
) -> Callable[[Request, Response], Awaitable[None]]:
    async def _dep(req: Request, _: Response) -> None:

        window_ms = cast(int, MAPPER_WINDOW_TIME.get(window_arg)) * 1000

        env_var = get_env()

        if env_var.py_env == "test":
            return

        async with redis_session() as r:
            ip = (
                (req.headers.get("x-forwarded-for", "")).split(",")[0]
                or getattr(req.client, "host", "")
            ).strip() or "unknown"

            now_ms = get_now()

            k = f"rl:{ip}:{req.url.path}"
            v = f"{now_ms}:{uuid.uuid4()}"

            await r.execute_command(
                "ZREMRANGEBYSCORE", k, 0, now_ms - window_ms
            )

            await r.execute_command("ZADD", k, now_ms, v)

            count = await r.execute_command("ZCARD", k) or 0

            await r.execute_command("EXPIRE", k, int((window_ms / 1000) + 1))

            remaining = max(0, limit - count)

            req.state.res_hdr = merge_exp_hdr(
                {
                    **getattr(req.state, "res_hdr", {}),
                    "RateLimit-Limit": str(limit),
                    "RateLimit-Remaining": str(remaining),
                    "RateLimit-Window": str(window_ms),
                }
            )

            if count > limit:
                oldest_req = await r.execute_command(
                    "ZRANGE", k, 0, 0, "WITHSCORES"
                )

                if oldest_req:
                    oldest_ms = int(float(oldest_req[1]))
                    reset_s = max(
                        0, math.ceil((oldest_ms + window_ms - now_ms) / 1000)
                    )
                else:
                    reset_s = int(window_ms / 1000)

                req.state.res_hdr["RateLimit-Reset"] = str(reset_s)

                raise ErrAPI(
                    status=429,
                    msg="Our hamster-powered server took a break"
                    " — try again later! 🐹",
                )

    return _dep
