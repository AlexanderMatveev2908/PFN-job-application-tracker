from fastapi import Request
from src.decorators.res import ResAPI


async def get_msg_ctrl(req: Request) -> ResAPI:

    return ResAPI.ok_200(
        msg="✅ get request ☎️",
    )


async def get_protected_data_ctrl(req: Request) -> ResAPI:
    return ResAPI.ok_200()
