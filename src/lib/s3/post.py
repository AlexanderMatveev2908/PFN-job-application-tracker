import datetime
from io import BytesIO
from pathlib import Path
from mypy_boto3_s3 import S3Client

from src.conf.aws.s3 import gen_s3_session
from ...conf.env import env_var


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
                "filename": file["filename"],
                # "name": Path(file["filename"]).stem,
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
        f"{env_var.aws_region_name}.amazonaws.com/{public_id}"
    )

    return {"public_id": public_id, "public_url": public_url}


async def upload_w3(v: dict | list[dict]) -> dict | list[dict]:

    async with gen_s3_session() as s3:

        if isinstance(v, list):
            return [await upload_single(f, s3) for f in v]
        else:
            return await upload_single(v, s3)
