import json
from typing import Callable

# import attr
from fastapi import Request
from ..lib.system import write_f
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp


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

        if (
            request.url.path.startswith(
                ("/docs", "/openapi.json", "/favicon.ico", "/redoc")
            )
            or not body
        ):
            return await call_next(request)

        try:
            parsed = json.loads(body)
            print(parsed)
        except Exception as err:
            print("❌ JSON parse error:", err)
            parsed = {"raw": body.decode("utf-8", errors="ignore")}

        obj = {
            "body": parsed,
            "params": dict(request.path_params),
            "query": dict(request.query_params),
            "access_token": request.headers.get("authorization"),
            "refresh_token": request.cookies.get("refresh_token"),
        }

        write_f(self.log_path, json.dumps(obj, indent=2))

        return await call_next(request)
