from typing import Any, Mapping, TypedDict
import datetime
from io import BytesIO
from pathlib import Path
from types_aiobotocore_s3 import S3Client

from src.conf.aws.s3 import gen_s3_session
from src.conf.env import env_var


class UploadRecord(TypedDict):
    content_type: str
    filename: str
    buffer: bytes | None
    path: str | None


async def upload_single(file: UploadRecord, s3: S3Client) -> dict:
    base_path = f"{env_var.app_name}"
    content_type = file["content_type"]

    public_id = str(
        Path(base_path)
        / ("videos" if content_type.startswith("video/") else "images")
        / file["filename"]
    )

    metadata: Mapping[str, str] = {
        "created_at": datetime.datetime.now().isoformat(),
        "filename": file["filename"],
    }
    extra_args: dict[str, Any] = {
        "ContentType": content_type,
        "Metadata": metadata,
    }

    if content_type.startswith("video/"):
        assert file["path"] is not None
        await s3.upload_file(
            file["path"],
            env_var.aws_bucket_name,
            public_id,
            ExtraArgs=extra_args,
        )
    else:
        assert file["buffer"] is not None
        buff_stream = BytesIO(file["buffer"])
        await s3.upload_fileobj(
            buff_stream,
            env_var.aws_bucket_name,
            public_id,
            ExtraArgs=extra_args,
        )

    public_url = (
        f"https://{env_var.aws_bucket_name}.s3."
        f"{env_var.aws_region_name}.amazonaws.com/{public_id}"
    )
    return {"public_id": public_id, "public_url": public_url}


async def upload_w3(v: UploadRecord | list[UploadRecord]) -> dict | list[dict]:
    async with gen_s3_session() as s3:
        if isinstance(v, list):
            return [await upload_single(f, s3) for f in v]
        else:
            return await upload_single(v, s3)
