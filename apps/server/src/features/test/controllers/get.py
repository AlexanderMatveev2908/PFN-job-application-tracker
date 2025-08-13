from fastapi import Request

from src.decorators.res import ResAPI


async def get_msg_ctrl(_: Request) -> ResAPI:
    return ResAPI.ok_200(msg="✅ get request ☎️")
