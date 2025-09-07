from typing import Awaitable, Callable
from fastapi import Request, UploadFile
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp
from src.lib.data_structure import parse_bool
from src.middleware.parsers.form_data_parser.lib import parse_file
from src.middleware.parsers.form_data_parser.types import (
    ParsedForm,
    ParsedItem,
    ParsedValue,
)


def assign_nested(d: dict, key: str, val: ParsedValue) -> None:
    parts = key.replace("]", "").split("[")

    curr = d
    stop = -2 if not parts[-1] else -1

    for p in parts[:stop]:
        curr = curr.setdefault(p, {})
    last = parts[-1]

    if not last:
        arr = curr.setdefault(parts[-2], [])
        if isinstance(arr, list):
            arr.append(val)
        else:
            curr[parts[-2]] = [arr, val]
    elif last in curr:
        existing = curr[last]
        if isinstance(existing, list):
            existing.append(val)
        else:
            curr[last] = [existing, val]
    else:
        curr[last] = val


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

            assign_nested(parsed_f, k, value)

        request.state.parsed_f = parsed_f
        return await call_next(request)
