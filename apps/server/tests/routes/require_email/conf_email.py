from httpx import AsyncClient
import pytest
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib, register_ok_lib, wrap_httpx

URL = "/require-email/confirm-email"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_require = await wrap_httpx(
        api,
        url=URL,
        data={"email": res_register["payload"]["email"]},
        expected_code=201,
    )

    assert "email sent" in res_require["data"]["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    await wrap_httpx(
        api,
        url=URL,
        data={"email": "<><>/!"},
        expected_code=422,
    )


@pytest.mark.asyncio
async def err_not_found_t(api: AsyncClient) -> None:
    res_require = await wrap_httpx(
        api,
        url=URL,
        data={"email": "non-existent@gmail.com"},
        expected_code=404,
    )

    assert "user not found" in res_require["data"]["msg"]


@pytest.mark.asyncio
async def err_already_confirmed_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.CONF_EMAIL,
    )

    res_verify = await wrap_httpx(
        api,
        url=f'/verify/confirm-email?cbc_hmac_token={res_tokens["cbc_hmac_token"]}',  # noqa: E501
        expected_code=200,
        method="GET",
    )

    assert "email verified" in res_verify["data"]["msg"]

    res_require_again = await wrap_httpx(
        api,
        url=URL,
        expected_code=409,
        data={"email": res_tokens["payload"]["email"]},
    )

    assert "user already verified" in res_require_again["data"]["msg"]
