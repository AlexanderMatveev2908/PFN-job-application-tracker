# from contextlib import asynccontextmanager
# from typing import Any, AsyncGenerator, Protocol, cast
# import aioboto3
# from src.constants.aws import aws_keys
# from aiobotocore.client import AioBaseClient


# class SESAsyncClient(Protocol):
#     async def send_email(self, **kwargs: Any) -> dict: ...
#     async def send_raw_email(self, **kwargs: Any) -> dict: ...


# @asynccontextmanager
# async def ses_session() -> AsyncGenerator[SESAsyncClient, None]:
#     session = aioboto3.Session()

#     async with cast(AioBaseClient, session.client("ses", **aws_keys)) as ses:
#         yield cast(SESAsyncClient, ses)
