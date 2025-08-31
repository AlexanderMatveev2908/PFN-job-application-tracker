import copy
import json
from typing import Callable

# import attr
from fastapi import Request

from src.lib.data_structure import is_obj_ok
from src.lib.logger import clg
from ...lib.system import write_f
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp


# @attr.s(auto_attribs=True)
class LoggerJSON(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, log_path: str = "logger/log.json"):
        super().__init__(app)
        self.log_path = log_path

    # app: ASGIApp
    # log_path: str = attr.ib(default="clger/clg.json")

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
            if "application/json" in request.headers.get("content-type", ""):
                parsed = json.loads(body)

        except Exception:
            ...
            # parsed = {"raw": body.decode("utf-8", errors="ignore")}

        parsed_q = (getattr(request.state, "parsed_q", None),)
        parsed_f = copy.deepcopy(getattr(request.state, "parsed_f", None))

        if parsed_f and parsed_f.get("images", {}):
            for idx, img in enumerate(parsed_f["images"]):
                parsed_f["images"][idx] = {
                    "filename": img["filename"],
                    "size": img["size"],
                    "content_type": img.get("content_type"),
                }

        params = dict(request.path_params)

        obj = {
            "body": parsed if is_obj_ok(parsed) else None,
            "params": params if is_obj_ok(params) else None,
            "parsed_q": parsed_q if is_obj_ok(parsed_q) else None,
            "parsed_f": parsed_f if is_obj_ok(parsed_f) else None,
            "access_token": request.headers.get("authorization"),
            "refresh_token": request.cookies.get("refresh_token"),
        }

        try:
            write_f(self.log_path, json.dumps(obj, indent=2))
        except Exception as err:
            clg(err, ttl="obj not serializable")

        async def receive() -> dict:
            return {
                "type": "http.request",
                "body": body,
                "more_body": False,
            }

        request = Request(request.scope, receive)

        return await call_next(request)
