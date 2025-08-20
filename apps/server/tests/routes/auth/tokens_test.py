import re
import pytest
from httpx import AsyncClient
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    await get_tokens_lib(
        api,
    )


@pytest.mark.asyncio
async def err_expired_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(api, reverse=True)
    url = f"/test/get-err-expired?cbc_hmac_token_t={TokenT.CONF_EMAIL.value}"

    res_jwt = await wrap_httpx(
        api,
        url=url,
        data={"token": res_tokens["access_token"], "act": "JWT"},
        expected_code=401,
    )
    assert "ACCESS_TOKEN_EXPIRED" in res_jwt["data"]["msg"]

    res_jwe = await wrap_httpx(
        api,
        url=url,
        data={"token": res_tokens["refresh_token"], "act": "JWE"},
        expected_code=401,
    )
    assert "REFRESH_TOKEN_EXPIRED" in res_jwe["data"]["msg"]

    res_cbc = await wrap_httpx(
        api,
        url=url,
        data={"token": res_tokens["cbc_hmac_token"], "act": "CBC_HMAC"},
        expected_code=401,
    )
    assert "CBC_HMAC_EXPIRED" in res_cbc["data"]["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(api, reverse=True)

    url = f"/test/get-err-invalid?cbc_hmac_token_t={TokenT.CONF_EMAIL.value}"

    res_jwt = await wrap_httpx(
        api,
        url=url,
        data={"token": res_tokens["access_token"][:-4] + "hack", "act": "JWT"},
        expected_code=401,
    )
    assert re.compile(r".*ACCESS_TOKEN_INVALID$").fullmatch(
        res_jwt["data"]["msg"]
    )

    res_jwe = await wrap_httpx(
        api,
        url=url,
        data={
            "token": res_tokens["refresh_token"][:-4] + "hack",
            "act": "JWE",
        },
        expected_code=401,
    )
    assert re.compile(r".*REFRESH_TOKEN_INVALID$").fullmatch(
        res_jwe["data"]["msg"]
    )

    res_cbc = await wrap_httpx(
        api,
        url=url,
        data={
            "token": res_tokens["cbc_hmac_token"][:-4] + "aaaa",
            "act": "CBC_HMAC",
        },
        expected_code=401,
    )
    assert re.compile(r".*CBC_HMAC_INVALID$").fullmatch(res_cbc["data"]["msg"])
