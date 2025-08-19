from httpx import AsyncClient
import pytest

from tests.conf.lib import register_ok_lib, wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_require = await wrap_httpx(
        api,
        url="/require-email/forgot-pwd",
        data={"email": res_register["payload"]["email"]},
        expected_code=201,
    )
