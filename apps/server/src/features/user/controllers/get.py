from fastapi import Request
from fastapi.responses import JSONResponse

from src.decorators.res import ResAPI


async def get_us_profile_ctrl(req: Request) -> JSONResponse:
    return ResAPI(req).ok_200()
