from fastapi import Request

from src.decorators.res import ResAPI


async def get_test(_: Request) -> ResAPI:

    return ResAPI.ok_200()
