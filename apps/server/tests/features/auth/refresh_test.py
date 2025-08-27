import pytest
from src.constants.reg import REG_JWT
from src.lib.etc import grab
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

URL_SENS = "/test/protected"
URL_REF = "/auth/refresh"


@pytest.mark.asyncio
async def ok_t(api) -> None:
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

    assrt_msg(res_err, "jwt_expired")

    await get_tokens_lib(api, existing_payload=res_tokens_expired["payload"])

    res_refresh = await wrap_httpx(
        api,
        url=URL_REF,
        expected_code=200,
        access_token=res_tokens_expired["access_token"],
        method="GET",
    )
    assert REG_JWT.fullmatch(grab(res_refresh, "access_token"))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "expected_msg",
    [
        "jwe_expired",
    ],
)
async def bad_cases_t(api: AsyncClient, expected_msg: str) -> None:
    await get_tokens_lib(api, reverse=True)

    res_err = await wrap_httpx(
        api,
        url=URL_REF,
        expected_code=401,
        method="GET",
    )

    assrt_msg(res_err, expected_msg)
