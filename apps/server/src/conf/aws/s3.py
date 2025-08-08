from contextlib import asynccontextmanager
from typing import AsyncGenerator, cast
import aioboto3
from types_aiobotocore_s3 import S3Client
from src.constants.aws import aws_keys
from aiobotocore.client import AioBaseClient


@asynccontextmanager
async def gen_s3_session() -> AsyncGenerator[S3Client, None]:
    session = aioboto3.Session()

    async with cast(AioBaseClient, session.client("s3", **aws_keys)) as s3:
        yield cast(S3Client, s3)
