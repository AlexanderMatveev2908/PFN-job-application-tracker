import pytest
from src.constants.reg import REG_JWT
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx

URL_SENS = "/test/protected"
URL_REF = "/auth/refresh"


@pytest.mark.asyncio
async def test_refresh_ok(api) -> None:
    res_tokens_expired = await get_tokens_lib(
        api, cbc_hmac_t=TokenT.CONF_EMAIL, reverse=True
    )

    res_err = await wrap_httpx(
        api,
        url=URL_SENS,
        expected_code=401,
        method="GET",
        access_token=res_tokens_expired["access_token"],
    )
    assert "access_token_expired" in res_err["data"]["msg"].lower()

    await get_tokens_lib(api, existing_payload=res_tokens_expired["payload"])

    res_refresh = await wrap_httpx(
        api,
        url=URL_REF,
        expected_code=200,
        access_token=res_tokens_expired["access_token"],
        method="GET",
    )
    assert REG_JWT.fullmatch(res_refresh["data"]["access_token"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "expected_msg",
    [
        "refresh_token_expired",
    ],
)
async def test_refresh_invalid_cases(api, expected_msg) -> None:
    await get_tokens_lib(api, reverse=True)

    res_err = await wrap_httpx(
        api,
        url=URL_REF,
        expected_code=401,
        method="GET",
    )
    assert expected_msg in res_err["data"]["msg"].lower()
