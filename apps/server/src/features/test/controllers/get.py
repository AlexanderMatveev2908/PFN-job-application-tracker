from fastapi import Request
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI


async def get_msg_ctrl(req: Request) -> ResAPI:

    raise ErrAPI(msg="some msg", status=401)

    return ResAPI.ok_200(
        msg="✅ get request ☎️",
    )
