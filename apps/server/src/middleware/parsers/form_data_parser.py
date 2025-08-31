from __future__ import annotations
import mimetypes
from pathlib import Path
from typing import Awaitable, Callable, Optional, TypedDict, Union, List
import uuid
import aiofiles
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp
from starlette.datastructures import UploadFile

from src.lib.data_structure import parse_bool
from ...lib.system import APP_DIR


UPLOAD_FIR = APP_DIR / "uploads"


class AppFile(TypedDict, total=False):
    content_type: Optional[str]
    size: float | None
    filename: Optional[str]
    buffer: Optional[bytes]
    path: Optional[str]


Primitive = str | bool
ParsedItem = Union[AppFile, Primitive]
ParsedList = List[ParsedItem]
ParsedValue = Union[ParsedItem, ParsedList]
ParsedForm = dict[str, ParsedValue]


def gen_filename(uf: UploadFile) -> str:
    name = str(uuid.uuid4())
    ext = (
        Path(uf.filename).suffix
        if uf.filename
        else mimetypes.guess_extension(uf.content_type or "")
    ) or ""
    return f"{name}{ext}"


async def gen_local_vid(uf: UploadFile) -> str:
    if not UPLOAD_FIR.exists():
        UPLOAD_FIR.mkdir(exist_ok=True)

    fp = UPLOAD_FIR / gen_filename(uf)

    async with aiofiles.open(fp, "wb") as out:
        while chunk := await uf.read(1024**2):
            await out.write(chunk)

    return str(fp)


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
                size_b = getattr(v, "size", 0)
                size_MB = (
                    round(size_b / (1024**2), ndigits=2) if size_b else None
                )

                file_rec: AppFile = {
                    "content_type": v.content_type,
                    "size": size_MB,
                }

                if v.content_type and v.content_type.startswith("video/"):
                    saved_path = await gen_local_vid(v)
                    file_rec.update(
                        {
                            "filename": Path(saved_path).name,
                            "path": saved_path,
                        }
                    )
                else:
                    file_rec.update(
                        {
                            "filename": gen_filename(v),
                            "buffer": await v.read(),
                        }
                    )

                value = file_rec
            else:
                value = parse_bool(v)

            existing = parsed_f.get(k)
            if existing is None:
                parsed_f[k] = value
            elif isinstance(existing, list):
                existing.append(value)
            else:
                parsed_f[k] = [existing, value]

        request.state.parsed_f = parsed_f
        return await call_next(request)
