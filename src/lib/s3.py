import datetime
from io import BytesIO
from mypy_boto3_s3 import S3Client

from src.conf.s3 import gen_s3_session
from ..conf.env import env_var


async def upload_single(file: dict, base_path: str, s3: S3Client) -> dict:
    content_type = file["content_type"]
    extra_args = {
        "ContentType": content_type,
        "Metadata": {
            "created_at": datetime.datetime.now().isoformat(),
        },
    }
    public_id = (
        f"{base_path}/{'videos' if 'video/' in content_type else 'images'}"
        f"/{file['filename']}"
    )
    args_aws = {
        "Bucket": env_var.aws_bucket_name,
        "Key": public_id,
        "ExtraArgs": extra_args,
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

        base_path = f"{env_var.app_name}"
        args = {"base_path": base_path, "s3": s3}

        if isinstance(v, list):
            return [await upload_single(f, **args) for f in v]
        else:
            return await upload_single(v, **args)


async def gen_presigned_url(public_id: str) -> str:
    async with gen_s3_session() as s3:
        return await s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": env_var.aws_bucket_name, "Key": public_id},
            ExpiresIn=60**2 * 24,
        )
