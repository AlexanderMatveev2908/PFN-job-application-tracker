from fastapi import Request, Response

from src.decorators.res import ResAPI


async def add_job_appl_ctrl(req: Request) -> Response:
    return ResAPI(req).ok_200()
