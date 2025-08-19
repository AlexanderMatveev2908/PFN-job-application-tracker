from httpx import AsyncClient
import pytest

from tests.conf.lib import register_ok_lib, wrap_httpx


@pytest.mark.asyncio
async def require_email_ok_t(api: AsyncClient) -> None:
    payload, *_ = await register_ok_lib(api)

    data_forgot_pwd, *_ = await wrap_httpx(
        api,
        data={"email": payload["email"]},
        url="/require-email/forgot-pwd",
        expected_code=201,
    )

    assert "email sent" in data_forgot_pwd["msg"]


@pytest.mark.asyncio
async def require_email_err_invalid_t(api: AsyncClient) -> None:
    pass
