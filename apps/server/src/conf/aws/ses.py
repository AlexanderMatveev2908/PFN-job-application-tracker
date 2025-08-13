from typing import AsyncGenerator, cast
import aioboto3
from src.constants.aws import aws_keys
from aiobotocore.client import AioBaseClient


async def ses_session() -> AsyncGenerator[AioBaseClient, None]:
    session = aioboto3.Session()

    async with cast(AioBaseClient, session.client("ses", **aws_keys)) as ses:
        yield ses
