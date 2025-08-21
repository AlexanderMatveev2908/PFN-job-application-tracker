from fastapi import Request
from src.decorators.res import ResAPI


async def get_access_account_ctrl(req: Request) -> ResAPI:
    return ResAPI.ok_200()
