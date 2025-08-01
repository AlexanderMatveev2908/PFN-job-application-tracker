from typing import Any, Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.responses import Response
from src.lib.data_structure import parse_bool


class ParserQuery(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        parsed_q: dict[str, Any] = {}

        for k in request.query_params:
            v = request.query_params.getlist(k)

            if len(v) > 1:
                parsed_q[k] = [parse_bool(el) for el in v]
            else:
                parsed_q[k] = parse_bool(v[0])

        request.state.parsed_q = parsed_q
        return await call_next(request)
