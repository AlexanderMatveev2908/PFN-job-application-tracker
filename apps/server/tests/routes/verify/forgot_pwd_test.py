from httpx import AsyncClient
import pytest

from src.models.token import TokenT
from tests.conf.lib import get_tokens_lib, wrap_httpx


URL = "/verify/forgot-pwd?cbc_hmac_token="


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:

    res_tokens = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.RECOVER_PWD,
    )

    res_check_tk = await wrap_httpx(
        api,
        url=f'{URL}{res_tokens["cbc_hmac_token"]}',  # noqa: E501
        expected_code=200,
        method="GET",
    )

    assert "verification successful" in res_check_tk["data"]["msg"]


@pytest.mark.asyncio
async def err_not_provided_t(api: AsyncClient) -> None:
    res_check = await wrap_httpx(
        api, url=f"{URL}", expected_code=401, method="GET"
    )

    assert "CBC_HMAC_NOT_PROVIDED" in res_check["data"]["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.RECOVER_PWD,
    )

    res_check = await wrap_httpx(
        api,
        url=f"{URL}{'hack' + res_tokens['cbc_hmac_token'][4:]}",
        expected_code=401,
        method="GET",
    )

    assert "CBC_HMAC_INVALID_FORMAT" in res_check["data"]["msg"]


@pytest.mark.asyncio
async def err_wrong_token_type_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.CHANGE_PWD,
    )

    res_check = await wrap_httpx(
        api,
        url=f"{URL}{res_tokens['cbc_hmac_token']}",
        expected_code=401,
        method="GET",
    )

    assert "CBC_HMAC_WRONG_TYPE" in res_check["data"]["msg"]
