from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
import aioboto3
from .aws import aws_keys


@asynccontextmanager
async def gen_ce_session() -> AsyncGenerator[Any, None]:
    session = aioboto3.Session()

    async with session.client(  # type: ignore type
        "ce",
        **aws_keys,  # type: ignore type
    ) as ce:
        yield ce
