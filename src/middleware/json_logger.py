import json
from typing import Callable, Dict

# import attr
from fastapi import Request
from ..lib.system import write_f
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp
from ..lib.logger import _cg


# @attr.s(auto_attribs=True)
class LoggerJSON(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, log_path="logger/log.json"):
        super().__init__(app)
        self.log_path = log_path

    # app: ASGIApp
    # log_path: str = attr.ib(default="logger/log.json")

    # def __attrs_post_init__(self):
    #     super().__init__(self.app)

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        body = await request.body()
        parsed = {}

        if request.url.path.startswith(
            ("/docs", "/openapi.json", "/favicon.ico", "/redoc")
        ):
            return await call_next(request)

        try:
            parsed = json.loads(body)

        except Exception as err:
            _cg(
                err,
                ttl="❌ JSON parse error:",
            )
            parsed = {"raw": body.decode("utf-8", errors="ignore")}

        obj = {
            "body": parsed,
            "params": dict(request.path_params),
            "psd_q": dict(request.state.psd_q),
            "access_token": request.headers.get("authorization"),
            "refresh_token": request.cookies.get("refresh_token"),
        }

        write_f(self.log_path, json.dumps(obj, indent=2))

        async def receive() -> Dict:
            return {"type": "http.request", "body": body, "more_body": False}

        request = Request(request.scope, receive)

        return await call_next(request)
