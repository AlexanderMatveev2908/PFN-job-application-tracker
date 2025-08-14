from fastapi import Request
from src.decorators.res import ResAPI


async def get_msg_ctrl(req: Request) -> ResAPI:

    return ResAPI.ok_200(
        msg="✅ get request ☎️",
        rate_limit=req.state.rate_limit_headers,
    )
