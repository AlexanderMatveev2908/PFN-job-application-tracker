from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
from starlette.responses import Response
from fastapi import HTTPException
from typing import Callable

from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.lib.logger import log_err


class WrapAPI(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as err:

            log_err(err)

            data = None

            if isinstance(err, HTTPException):
                status = err.status_code
                msg = err.detail
            elif isinstance(err, ErrAPI):
                status = err.status
                msg = err.msg
                data = getattr(err, "data", None)
            else:
                status = 500
                msg = str(err)

            return ResAPI(request).err_ctm(
                status=status,
                msg=msg,
                data=data or {},
            )
