import json
from typing import Any, Dict

from fastapi import Request


async def get_test(req: Request) -> Dict[str, Any]:
    b = json.loads(await req.body())
    parsed_q = getattr(req.state, "parsed_q", None)

    return {
        "msg": "all worked fine ✅",
        "parsed_q": parsed_q,
        "body": b,
    }
