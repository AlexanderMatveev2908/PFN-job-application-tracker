from fastapi import Request

from src.decorators.res import ResAPI


async def get_test(req: Request) -> ResAPI:

    return ResAPI.ok_200()
