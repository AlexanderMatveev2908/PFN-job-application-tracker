from typing import AsyncGenerator, cast
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from src.__dev_only.db.delete import clean_tables
from src.server import app
from src.conf.env import env_var


async def client(clean: bool = True) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url=cast(str, env_var.next_public_back_url_dev),
    ) as c:
        if clean:
            await clean_tables()
        yield c


@pytest_asyncio.fixture
async def dirty_api() -> AsyncGenerator[AsyncClient, None]:
    async for c in client(clean=False):
        yield c


@pytest_asyncio.fixture
async def api() -> AsyncGenerator[AsyncClient, None]:
    async for c in client():
        yield c
