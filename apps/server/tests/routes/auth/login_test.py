from httpx import AsyncClient
import pytest

from src.constants.reg import REG_JWE, REG_JWT
from tests.conf.constants import get_payload_register
from tests.conf.lib.etc import (
    extract_login_payload,
    register_ok_lib,
    wrap_httpx,
)


URL = "/auth/login"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_login = await wrap_httpx(
        api,
        url=URL,
        data=extract_login_payload(res_register["payload"]),
        expected_code=200,
    )

    assert REG_JWE.fullmatch(res_login["refresh_token"])
    assert REG_JWT.fullmatch(res_login["data"]["access_token"])


@pytest.mark.asyncio
async def err_not_found_t(api: AsyncClient) -> None:
    res_login = await wrap_httpx(
        api,
        url=URL,
        data=extract_login_payload(get_payload_register()),
        expected_code=404,
    )

    assert "user not found" in res_login["data"]["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_login = await wrap_httpx(
        api,
        url=URL,
        data={
            **extract_login_payload(res_register["payload"]),
            "password": res_register["payload"]["password"] + "yayyyy",
        },
        expected_code=401,
    )

    assert "invalid credentials" in res_login["data"]["msg"]
