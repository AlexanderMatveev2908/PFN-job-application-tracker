from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, cast
import aioboto3
from aiobotocore.client import AioBaseClient
from src.constants.aws import aws_keys


@asynccontextmanager
async def gen_ce_session() -> AsyncGenerator[Any, None]:
    session = aioboto3.Session()

    async with cast(
        AioBaseClient,
        session.client(
            "ce",
            **aws_keys,
        ),
    ) as ce:
        yield ce
