import aioboto3
from .env import env_var


async def upload_w3(v: dict | list[dict]) -> dict | list[dict]:
    async with aioboto3.client(  # type: ignore[attr-defined]
        "s3",
        aws_access_key_id=env_var.aws_access_key,
        aws_secret_access_key=env_var.aws_access_secret_key,
        region_name=env_var.aws_region,
    ) as s3:

        async def upload_single(file: dict) -> dict:
            content_type = file["content_type"]
