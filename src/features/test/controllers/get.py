import json

from fastapi import Request

from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI


async def get_test(req: Request) -> ResAPI:
    b = json.loads(await req.body())

    raise ErrAPI(
        status=403,
        msg="some long desc...",
    )

    return ResAPI.ok_200(
        body=b,
    )
