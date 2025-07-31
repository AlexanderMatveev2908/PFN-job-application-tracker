from typing import Any, Dict

from fastapi import Request


async def get_test(req: Request) -> Dict[str, Any]:
    b = await req.body()

    return {
        "msg": "all worked fine ✅",
        "psd_q": getattr(req.state, "psd_q", None),
        "body": b,
    }
