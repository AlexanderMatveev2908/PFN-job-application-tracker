from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp


class FormDataParser(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        content_t = request.headers.get("content-type", "")

        if "multipart/form-data" not in content_t:
            return await call_next(request)

        return await call_next(request)
