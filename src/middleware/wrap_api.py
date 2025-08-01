import traceback
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
from starlette.responses import Response
from fastapi import HTTPException
from typing import Callable

from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from ..lib.logger import log


class WrapAPI(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as err:

            frames = traceback.extract_tb(err.__traceback__)
            src_frames = []

            for f in frames:
                if "src/" in f.filename:
                    src_frames.append(
                        f"📂 {f.filename} => 🔢 {f.lineno}"
                        f" | 🆎 {f.name} | ☢️ {f.line}"
                    )

            log(
                *src_frames,
                "\t",
                f"💣 {type(err).__name__}",
                ttl="💥 global err",
            )

            opt = None

            if isinstance(err, HTTPException):
                status = err.status_code
                msg = err.detail
            elif isinstance(err, ErrAPI):
                status = err.status
                msg = err.msg
                opt = getattr(err, "opt", None)
            else:
                status = 500
                msg = str(err)

            return ResAPI.err_ctm(status=status, msg=msg, opt=opt)
