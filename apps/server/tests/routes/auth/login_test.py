from httpx import AsyncClient
import pytest

from src.constants.reg import REG_JWE, REG_JWT
from tests.conf.constants import get_payload_register
from tests.conf.lib import extract_login_payload, register_ok_lib, wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    payload, *_ = await register_ok_lib(api)

    data_login, refresh_token = await wrap_httpx(
        api,
        url="/auth/login",
        data=extract_login_payload(payload),
        expected_code=200,
    )

    assert REG_JWE.fullmatch(refresh_token)
    assert REG_JWT.fullmatch(data_login["access_token"])


@pytest.mark.asyncio
async def err_not_found_t(api: AsyncClient) -> None:
    data, *_ = await wrap_httpx(
        api,
        url="/auth/login",
        data=extract_login_payload(get_payload_register()),
        expected_code=404,
    )

    assert "user not found" in data["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    payload, *_ = await register_ok_lib(api)

    data_login, *_ = await wrap_httpx(
        api,
        url="/auth/login",
        data={
            **extract_login_payload(payload),
            "password": payload["password"] + "yayyyy",
        },
        expected_code=401,
    )

    assert "invalid credentials" in data_login["msg"]
