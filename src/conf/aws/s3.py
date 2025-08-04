from contextlib import asynccontextmanager
from typing import AsyncGenerator
import aioboto3
from mypy_boto3_s3 import S3Client
from .aws import aws_keys


@asynccontextmanager
async def gen_s3_session() -> AsyncGenerator[S3Client, None]:
    session = aioboto3.Session()

    async with session.client("s3", **aws_keys) as s3:  # type: ignore
        yield s3
