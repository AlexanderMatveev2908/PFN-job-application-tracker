from fastapi import Request

from src.decorators.res import ResAPI


async def change_pwd_ctrl(
    req: Request,
) -> ResAPI:
    return ResAPI.ok_200()
