from fastapi import Request

from src.decorators.res import ResAPI


async def confirm_new_email_ctrl(req: Request) -> ResAPI:
    return ResAPI.ok_200()
