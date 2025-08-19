from httpx import AsyncClient
import pytest

from tests.conf.lib import register_ok_lib, wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res = await register_ok_lib(api)

    data_forgot_pwd, *_ = await wrap_httpx(
        api,
        data={"email": res["payload"]["email"]},
        url="/require-email/forgot-pwd",
        expected_code=201,
    )

    assert "email sent" in data_forgot_pwd["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    res = await register_ok_lib(api)

    data, *_ = await wrap_httpx(
        api,
        url="/require-email/forgot-pwd",
        data={"email": res["payload"]["email"] * 8},
        expected_code=422,
    )


@pytest.mark.asyncio
async def err_404_t(api: AsyncClient) -> None:

    data, *_ = await wrap_httpx(
        api,
        url="/require-email/forgot-pwd",
        data={"email": "example-non-existent@gmail.com"},
        expected_code=404,
    )

    assert "user not found" in data["msg"]
