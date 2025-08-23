from fastapi import Request

from src.decorators.res import ResAPI


async def delete_account_ctrl(req: Request) -> ResAPI:
    return ResAPI.ok_200()
