import json

from fastapi import Request

from src.decorators.res import AppRes


async def get_test(req: Request) -> AppRes:
    b = json.loads(await req.body())
    parsed_q = getattr(req.state, "parsed_q", None)

    return AppRes.ok_200(
        body=b,
        parsed_q=parsed_q,
    )
