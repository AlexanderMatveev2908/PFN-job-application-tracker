import re
import pytest
from httpx import AsyncClient
from src.models.token import TokenT
from tests.conf.lib import get_tokens_lib, wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    await get_tokens_lib(api, health=True)


@pytest.mark.asyncio
async def err_expired_t(api: AsyncClient) -> None:
    res = await get_tokens_lib(api)
    url = f"/test/get-err-expired?cbc_hmac_token_t={TokenT.CONF_EMAIL.value}"

    data_jwt, _ = await wrap_httpx(
        api,
        url=url,
        data={"token": res["access_token"], "act": "JWT"},
        expected_code=401,
    )
    assert "ACCESS_TOKEN_EXPIRED" in data_jwt["msg"]

    data_jwe, _ = await wrap_httpx(
        api,
        url=url,
        data={"token": res["refresh_token"], "act": "JWE"},
        expected_code=401,
    )
    assert "REFRESH_TOKEN_EXPIRED" in data_jwe["msg"]

    data_cbc, _ = await wrap_httpx(
        api,
        url=url,
        data={"token": res["cbc_hmac_token"], "act": "CBC_HMAC"},
        expected_code=401,
    )
    assert "CBC_HMAC_EXPIRED" in data_cbc["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    res = await get_tokens_lib(api)

    url = f"/test/get-err-invalid?cbc_hmac_token_t={TokenT.CONF_EMAIL.value}"

    data_jwt, _ = await wrap_httpx(
        api,
        url=url,
        data={"token": res["access_token"][:-4] + "hack", "act": "JWT"},
        expected_code=401,
    )
    assert re.compile(r".*ACCESS_TOKEN_INVALID$").fullmatch(data_jwt["msg"])

    data_jwe, _ = await wrap_httpx(
        api,
        url=url,
        data={"token": res["refresh_token"][:-4] + "hack", "act": "JWE"},
        expected_code=401,
    )
    assert re.compile(r".*REFRESH_TOKEN_INVALID$").fullmatch(data_jwe["msg"])

    data_cbc, _ = await wrap_httpx(
        api,
        url=url,
        data={
            "token": res["cbc_hmac_token"][:-4] + "aaaa",
            "act": "CBC_HMAC",
        },
        expected_code=401,
    )
    assert re.compile(r".*CBC_HMAC_INVALID$").fullmatch(data_cbc["msg"])
