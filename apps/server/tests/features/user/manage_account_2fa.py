from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None: ...
