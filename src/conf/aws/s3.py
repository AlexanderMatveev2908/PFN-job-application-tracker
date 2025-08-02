from contextlib import asynccontextmanager
from typing import AsyncGenerator
import aioboto3
from mypy_boto3_s3 import S3Client
from .aws import aws_keys


@asynccontextmanager
async def gen_s3_session() -> AsyncGenerator[S3Client, None]:
    session = aioboto3.Session()

    async with session.client(  # type: ignore[func-returns-value]
        "s3", **aws_keys  # type: ignore
    ) as s3:
        yield s3
