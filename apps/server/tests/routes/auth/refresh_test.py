from httpx import AsyncClient
import pytest

from src.constants.reg import REG_JWT
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx

URL_SENS = "/test/protected"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
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

    assert "ACCESS_TOKEN_EXPIRED" in res_err["data"]["msg"]

    # __ I just grab a fresh JWE so I will have a valid refresh token to receive a new JWT # noqa: E501
    await get_tokens_lib(
        api,
        existing_payload=res_tokens_expired["payload"],
    )

    res_refresh = await wrap_httpx(
        api,
        url="/auth/refresh",
        expected_code=200,
        access_token=res_tokens_expired["access_token"],
        method="GET",
    )

    assert REG_JWT.fullmatch(res_refresh["data"]["access_token"])
