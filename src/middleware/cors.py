from dataclasses import dataclass
from typing import Callable

# import attr
from fastapi import Request
from src.decorators.res import ResAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp


# __ I am undecided which approach to use in classes 🧐
# __ I am thinking which would help me more between:
# __ dataclasses
# __ attrs
# __ raw python
# @attr.define
@dataclass
class CorsMDW(BaseHTTPMiddleware):
    app: ASGIApp
    whitelist: list[str]
    # def __init__(self, app: ASGIApp, whitelist: list[str]) -> None:
    # super().__init__(app)
    # self.whitelist = whitelist

    def __post_init__(self) -> None:
        super().__init__(self.app)

    # def __attrs_post_init__(self) -> None:
    # super().__init__(self.app)

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response | ResAPI:

        origin = request.headers.get("origin")

        if origin and not any(origin.startswith(w) for w in self.whitelist):
            return ResAPI.err_403(msg=f"{origin} not allowed 🚫")

        return await call_next(request)
