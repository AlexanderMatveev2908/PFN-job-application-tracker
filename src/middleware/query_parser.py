from typing import Any, Callable, Dict
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.responses import Response


class ParserQuery(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        psd_q: Dict[str, Any] = {}

        for k in request.query_params.keys():
            v = request.query_params.getlist(k)
            psd_q[k] = v if len(v) > 1 else v[0]

        request.state.psd_q = psd_q

        return await call_next(request)
