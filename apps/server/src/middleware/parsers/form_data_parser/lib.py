import mimetypes
from pathlib import Path
import uuid
import aiofiles
from fastapi import UploadFile

from src.lib.system import APP_DIR
from src.middleware.parsers.form_data_parser.types import AppFile

UPLOAD_DIR = APP_DIR / "uploads"


def gen_filename(uf: UploadFile) -> str:
    name = str(uuid.uuid4())
    ext = (
        Path(uf.filename).suffix
        if uf.filename
        else mimetypes.guess_extension(uf.content_type or "")
    ) or ""
    return f"{name}{ext}"


async def gen_local_vid(uf: UploadFile) -> str:
    if not UPLOAD_DIR.exists():
        UPLOAD_DIR.mkdir(exist_ok=True)

    fp = UPLOAD_DIR / gen_filename(uf)

    async with aiofiles.open(fp, "wb") as out:
        while chunk := await uf.read(1024**2):
            await out.write(chunk)

    return str(fp)


async def parse_file(v: UploadFile) -> AppFile:
    size_b = getattr(v, "size", 0)
    size_MB = round(size_b / (1024**2), ndigits=2) if size_b else None

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

    return file_rec
