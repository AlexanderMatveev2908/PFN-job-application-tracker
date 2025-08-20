from httpx import AsyncClient
import pytest

from tests.conf.lib.etc import register_ok_lib
from tests.conf.lib.idx import wrap_httpx

URL = "/require-email/forgot-pwd"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_forgot_pwd = await wrap_httpx(
        api,
        data={"email": res_register["payload"]["email"]},
        url=URL,
        expected_code=201,
    )

    assert "email sent" in res_forgot_pwd["data"]["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    await wrap_httpx(
        api,
        url=URL,
        data={"email": res_register["payload"]["email"] * 8},
        expected_code=422,
    )


@pytest.mark.asyncio
async def err_404_t(api: AsyncClient) -> None:

    res = await wrap_httpx(
        api,
        url=URL,
        data={"email": "example-non-existent@gmail.com"},
        expected_code=404,
    )

    assert "user not found" in res["data"]["msg"]
