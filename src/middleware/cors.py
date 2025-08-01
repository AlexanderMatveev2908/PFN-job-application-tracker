from typing import Callable
from fastapi import Request
from src.decorators.res import ResAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp
from ..constants.api import whitelist


class CorsMDW(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response | ResAPI:

        origin = request.headers.get("origin")

        if origin and not any(origin.startswith(w) for w in whitelist):
            return ResAPI.err_403(msg=f"{origin} not allowed 🚫")

        return await call_next(request)
