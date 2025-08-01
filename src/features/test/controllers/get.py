import json
from fastapi import Request

from src.decorators.res import ResAPI


async def get_test(req: Request) -> ResAPI:
    b = json.loads(await req.body())

    return ResAPI.ok_200(
        body=b,
    )
