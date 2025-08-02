import datetime
from io import BytesIO
import mimetypes
from pathlib import Path
import uuid
from mypy_boto3_s3 import S3Client

from src.conf.s3 import gen_s3_session
from src.lib.logger import clg
from ..conf.env import env_var


async def upload_single(file: dict, s3: S3Client) -> dict:
    base_path = f"{env_var.app_name}"
    content_type = file["content_type"]

    public_id = str(
        Path(base_path)
        / ("videos" if content_type.startswith("video/") else "images")
        / file["filename"]
    )

    args_aws = {
        "Bucket": env_var.aws_bucket_name,
        "Key": public_id,
        "ExtraArgs": {
            "ContentType": content_type,
            "Metadata": {
                "created_at": datetime.datetime.now().isoformat(),
            },
        },
    }

    if "video/" in content_type:
        await s3.upload_file(  # type: ignore[func-returns-value]
            file["path"], **args_aws
        )
    else:
        buff_stream = BytesIO(file["buffer"])
        await s3.upload_fileobj(  # type: ignore[func-returns-value]
            buff_stream, **args_aws
        )

    public_url = (
        f"https://{env_var.aws_bucket_name}.s3."
        f"{env_var.aws_region}.amazonaws.com/{public_id}"
    )

    return {"public_id": public_id, "public_url": public_url}


async def upload_w3(v: dict | list[dict]) -> dict | list[dict]:

    async with gen_s3_session() as s3:

        if isinstance(v, list):
            return [await upload_single(f, s3) for f in v]
        else:
            return await upload_single(v, s3)


async def gen_presigned_url(public_id: str) -> str:
    async with gen_s3_session() as s3:
        return await s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": env_var.aws_bucket_name, "Key": public_id},
            ExpiresIn=60**2 * 24,
        )


async def get_asset(public_id: str) -> None:
    async with gen_s3_session() as s3:
        res = await s3.get_object(
            Bucket=env_var.aws_bucket_name, Key=public_id
        )

        obj = {
            "public_id": public_id,
            "content_type": res["ContentType"],
            "size": res["ContentLength"],
            "metadata": res.get("Metadata"),
        }

        ext = mimetypes.guess_extension(obj["content_type"]) or ""
        # body_b = await res["Body"].read()
        file_dir = Path.cwd() / "assets"
        file_dir.mkdir(exist_ok=True)
        file_p = file_dir / f"{uuid.uuid4()}{ext}"
        # file_p.write_bytes(body_b)

        stream = res["Body"]
        with file_p.open("wb") as f:
            while chunk := await stream.read(1024**2):
                f.write(chunk)


async def gen_list_assets(prefix: str = "") -> None:
    async with gen_s3_session() as s3:
        res = await s3.get_objects_v2(
            Bucket=env_var.aws_bucket_name, Prefix=prefix
        )

        clg(res)
