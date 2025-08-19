import re
import pytest
from httpx import AsyncClient

from src.constants.reg import REG_CBC_HMAC, REG_JWE, REG_JWT
from tests.conf.constants import get_payload_register

from tests.conf.lib import get_tokens, wrap_httpx


@pytest.mark.asyncio
async def tokens_health_t(api: AsyncClient) -> None:
    await get_tokens(api, health=True)


@pytest.mark.asyncio
async def check_expired_t(api: AsyncClient) -> None:
    data_exp, _ = await wrap_httpx(
        api,
        url="/test/get-tokens-expired",
        data=get_payload_register(),
        expected_code=200,
    )

    assert REG_JWT.fullmatch(data_exp["access_token"])
    assert REG_JWE.fullmatch(data_exp["refresh_token"])
    assert REG_CBC_HMAC.fullmatch(data_exp["cbc_hmac_token"])

    url = "/test/get-err-expired"

    data_jwt, _ = await wrap_httpx(
        api,
        url=url,
        data={"token": data_exp["access_token"], "act": "JWT"},
        expected_code=401,
    )
    assert "ACCESS_TOKEN_EXPIRED" in data_jwt["msg"]

    data_jwe, _ = await wrap_httpx(
        api,
        url=url,
        data={"token": data_exp["refresh_token"], "act": "JWE"},
        expected_code=401,
    )
    assert "REFRESH_TOKEN_EXPIRED" in data_jwe["msg"]

    data_cbc, _ = await wrap_httpx(
        api,
        url=url,
        data={"token": data_exp["cbc_hmac_token"], "act": "CBC_HMAC"},
        expected_code=401,
    )
    assert "CBC_HMAC_EXPIRED" in data_cbc["msg"]


@pytest.mark.asyncio
async def check_invalid_t(api: AsyncClient) -> None:
    tokens, _ = await wrap_httpx(
        api,
        url="/test/tokens-health",
        data=get_payload_register(),
        expected_code=200,
    )

    url = "/test/get-err-invalid"

    data_jwt, _ = await wrap_httpx(
        api,
        url=url,
        data={"token": tokens["access_token"][:-4] + "hack", "act": "JWT"},
        expected_code=401,
    )
    assert "ACCESS_TOKEN_INVALID" in data_jwt["msg"]

    data_jwe, _ = await wrap_httpx(
        api,
        url=url,
        data={"token": tokens["refresh_token"][:-4] + "hack", "act": "JWE"},
        expected_code=401,
    )
    assert "REFRESH_TOKEN_INVALID" in data_jwe["msg"]

    data_cbc, _ = await wrap_httpx(
        api,
        url=url,
        data={
            "token": tokens["cbc_hmac_token"][:-4] + "aaaa",
            "act": "CBC_HMAC",
        },
        expected_code=401,
    )
    assert re.compile(r".*\sCBC_HMAC_INVALID$").fullmatch(data_cbc["msg"])
