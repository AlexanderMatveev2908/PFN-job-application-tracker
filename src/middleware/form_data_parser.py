import mimetypes
from pathlib import Path
from typing import Callable
import uuid
import aiofiles
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp
from starlette.datastructures import UploadFile
from ..lib.system import app_dir


UPLOAD_FIR = app_dir / "uploads/"


def gen_filename(uf: UploadFile) -> str:
    name = str(uuid.uuid4())
    # name = p.stem
    ext = (
        Path(uf.filename).suffix
        if uf.filename
        else mimetypes.guess_extension(uf.content_type or "")
    )

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
        self, request: Request, call_next: Callable
    ) -> Response:
        content_t = request.headers.get("content-type", "")

        if "multipart/form-data" not in content_t:
            return await call_next(request)

        parsed_f = {}
        form = await request.form()

        for k, v in form.multi_items():
            if isinstance(v, UploadFile):
                if v.content_type and v.content_type.startswith("video/"):
                    saved_path = await gen_local_vid(v)

                    value = {
                        "filename": Path(saved_path).name,
                        "content_type": v.content_type,
                        "size": getattr(v, "size", None),
                        "path": saved_path,
                    }
                else:
                    value = {
                        "filename": gen_filename(v),
                        "content_type": v.content_type,
                        "size": getattr(v, "size", None),
                    }
            else:
                value = v

            if k in parsed_f:
                if isinstance(parsed_f[k], list):
                    parsed_f[k].append(value)
                else:
                    parsed_f[k] = [parsed_f[k], value]
            else:
                parsed_f[k] = value

        request.state.parsed_f = parsed_f

        return await call_next(request)
