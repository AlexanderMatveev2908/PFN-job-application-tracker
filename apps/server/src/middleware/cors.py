from dataclasses import dataclass
from typing import Callable

# import attr
from fastapi import Request
from fastapi.responses import Response
from src.decorators.res import ResAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


# ? I am undecided which approach to use in classes 🧐
# ? I am thinking which would help me more between:
# ? dataclasses
# ? attrs
# ? raw python
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
    ) -> Response:

        origin = request.headers.get("origin")

        if origin and not any(origin.startswith(w) for w in self.whitelist):
            return ResAPI(request).err_403(msg=f"{origin} not allowed 🚫")

        return await call_next(request)
