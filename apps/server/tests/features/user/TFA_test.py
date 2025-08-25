from httpx import AsyncClient
import pytest

from tests.conf.lib.etc import gen_verified_user_lib


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res = await gen_verified_user_lib(api)
