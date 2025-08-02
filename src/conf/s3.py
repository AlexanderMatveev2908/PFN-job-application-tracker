from contextlib import asynccontextmanager
import aioboto3
from .env import env_var


@asynccontextmanager
async def gen_s3_session():
    session = aioboto3.Session()

    async with session.client(  # type: ignore[func-returns-value]
        "s3",
        aws_access_key_id=env_var.aws_access_key,
        aws_secret_access_key=env_var.aws_access_secret_key,
        region_name=env_var.aws_region,
    ) as s3:
        yield s3
