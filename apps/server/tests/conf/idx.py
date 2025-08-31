from typing import AsyncGenerator, cast
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from src.conf.env import get_env
from src.server import app


env_var = get_env()


async def client(clean: bool = True) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url=cast(str, env_var.next_public_back_url_test),
        follow_redirects=True,
    ) as c:
        if clean:
            pass
        yield c


@pytest_asyncio.fixture
async def dirty_api() -> AsyncGenerator[AsyncClient, None]:
    async for c in client(clean=False):
        yield c


@pytest_asyncio.fixture
async def api() -> AsyncGenerator[AsyncClient, None]:
    async for c in client():
        yield c
