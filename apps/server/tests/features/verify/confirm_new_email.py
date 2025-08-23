import os
from httpx import AsyncClient
import pytest

from src.constants.reg import REG_JWE, REG_JWT
from src.models.token import TokenT
from tests.conf.constants import RegisterPayloadT
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx

URL = "/verify/new-email?cbc_hmac_token="


async def _local_wrapper(api) -> RegisterPayloadT:
    res_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)

    new_email = os.urandom(15).hex() + "@gmail.com"

    res_change = await wrap_httpx(
        api,
        url="/user/change-email",
        access_token=res_tk["access_token"],
        data={"email": new_email, "cbc_hmac_token": res_tk["cbc_hmac_token"]},
        expected_code=200,
        method="PATCH",
    )

    assert "email sent to new address" in res_change["data"]["msg"]

    return res_tk["payload"]


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:

    res_tk_body = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.CHANGE_EMAIL,
        existing_payload=await _local_wrapper(api),
    )

    res_verify = await wrap_httpx(
        api,
        url=f'{URL}{res_tk_body["cbc_hmac_token"]}',
        method="GET",
        expected_code=200,
    )

    assert "email updated successfully" in res_verify["data"]["msg"]
    assert REG_JWT.fullmatch(res_verify["data"]["access_token"])
    assert REG_JWE.fullmatch(res_verify["refresh_token"])


@pytest.mark.asyncio
async def err_wrong_type_t(api: AsyncClient) -> None:
    res_tk_body = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.CONF_EMAIL,
        existing_payload=await _local_wrapper(api),
    )

    res_verify = await wrap_httpx(
        api,
        url=f'{URL}{res_tk_body["cbc_hmac_token"]}',
        method="GET",
        expected_code=401,
    )

    assert "CBC_HMAC_WRONG_TYPE" in res_verify["data"]["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    res_tk_body = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.CHANGE_EMAIL,
        existing_payload=await _local_wrapper(api),
    )

    res_verify = await wrap_httpx(
        api,
        url=f'{URL}{res_tk_body["cbc_hmac_token"][:-10]+os.urandom(5).hex()}',
        method="GET",
        expected_code=401,
    )

    assert "CBC_HMAC_INVALID" in res_verify["data"]["msg"]


@pytest.mark.asyncio
async def err_expired_t(api: AsyncClient) -> None:

    res_tk_body = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.CHANGE_EMAIL,
        existing_payload=await _local_wrapper(api),
        reverse=True,
    )

    res_verify = await wrap_httpx(
        api,
        url=f'{URL}{res_tk_body["cbc_hmac_token"]}',
        method="GET",
        expected_code=401,
    )

    assert "CBC_HMAC_EXPIRED" in res_verify["data"]["msg"]
