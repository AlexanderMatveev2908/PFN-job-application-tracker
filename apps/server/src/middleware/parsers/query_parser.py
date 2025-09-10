from typing import Any, Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.responses import Response

from src.lib.data_structure.parsers import assign_nested_parser, parse_bool


class ParserQuery(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        parsed_q: dict[str, Any] = {}

        for k, v in request.query_params.multi_items():
            assign_nested_parser(parsed_q, k, parse_bool(v))

        request.state.parsed_q = parsed_q
        return await call_next(request)
