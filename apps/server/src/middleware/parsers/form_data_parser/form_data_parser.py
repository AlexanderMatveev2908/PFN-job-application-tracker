from typing import Awaitable, Callable
from fastapi import Request, UploadFile
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp
from src.lib.data_structure.parsers import assign_nested_parser, parse_bool
from src.middleware.parsers.form_data_parser.lib import parse_file
from src.middleware.parsers.form_data_parser.types import (
    ParsedForm,
    ParsedItem,
)


class FormDataParser(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        content_t = request.headers.get("content-type", "")
        if "multipart/form-data" not in content_t:
            return await call_next(request)

        parsed_f: ParsedForm = {}
        form = await request.form()

        for k, v in form.multi_items():
            value: ParsedItem

            if isinstance(v, UploadFile):
                value = await parse_file(v)
            else:
                value = parse_bool(v)

            assign_nested_parser(parsed_f, k, value)

        request.state.parsed_f = parsed_f
        return await call_next(request)
