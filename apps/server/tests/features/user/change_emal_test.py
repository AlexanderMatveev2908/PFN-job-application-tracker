import os
from httpx import AsyncClient
import pytest

from src.constants.reg import REG_CBC_HMAC
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib, login_ok_lib, register_ok_lib
from tests.conf.lib.idx import wrap_httpx

URL = "/user/change-email"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_manage = await wrap_httpx(
        api,
        url="/user/manage-account",
        data={"password": res_register["payload"]["password"]},
        access_token=res_register["access_token"],
        expected_code=200,
    )

    assert REG_CBC_HMAC.fullmatch(res_manage["data"]["cbc_hmac_token"])

    new_email = os.urandom(20).hex() + "@gmail.com"

    res_mail = await wrap_httpx(
        api,
        url=URL,
        data={
            "email": new_email,
            "cbc_hmac_token": res_manage["data"]["cbc_hmac_token"],
        },
        access_token=res_register["access_token"],
        expected_code=200,
        method="PATCH",
    )

    assert "email sent to new address" in res_mail["data"]["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    res_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)

    res_err_jwt = await wrap_httpx(
        api,
        url=URL,
        data={
            "email": res_tk["payload"]["email"],
            "cbc_hmac_token": res_tk["cbc_hmac_token"],
        },
        access_token=res_tk["access_token"][:-4] + "abcd",
        expected_code=401,
        method="PATCH",
    )

    assert "ACCESS_TOKEN_INVALID" in res_err_jwt["data"]["msg"]

    res_err_cbc = await wrap_httpx(
        api,
        url=URL,
        data={
            "email": res_tk["payload"]["email"],
            "cbc_hmac_token": res_tk["cbc_hmac_token"][:-4] + "abcd",
        },
        access_token=res_tk["access_token"],
        expected_code=401,
        method="PATCH",
    )

    assert "CBC_HMAC_INVALID" in res_err_cbc["data"]["msg"]


@pytest.mark.asyncio
async def err_expired_t(api: AsyncClient) -> None:
    expired_tk = await get_tokens_lib(
        api, cbc_hmac_t=TokenT.MANAGE_ACC, reverse=True
    )

    res_login = await login_ok_lib(api, register_payload=expired_tk["payload"])

    res_err_jwt = await wrap_httpx(
        api,
        url=URL,
        data={
            "email": expired_tk["payload"]["email"],
            "cbc_hmac_token": expired_tk["cbc_hmac_token"],
        },
        access_token=expired_tk["access_token"],
        expected_code=401,
        method="PATCH",
    )

    assert "ACCESS_TOKEN_EXPIRED" in res_err_jwt["data"]["msg"]

    res_err_cbc = await wrap_httpx(
        api,
        url=URL,
        data={
            "email": expired_tk["payload"]["email"],
            "cbc_hmac_token": expired_tk["cbc_hmac_token"],
        },
        access_token=res_login["access_token"],
        expected_code=401,
        method="PATCH",
    )

    assert "CBC_HMAC_EXPIRED" in res_err_cbc["data"]["msg"]


@pytest.mark.asyncio
async def err_existing_t(api: AsyncClient) -> None:
    res_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)

    res_register = await register_ok_lib(api)

    res_err_same = await wrap_httpx(
        api,
        url=URL,
        data={
            "email": res_tk["payload"]["email"],
            "cbc_hmac_token": res_tk["cbc_hmac_token"],
        },
        access_token=res_tk["access_token"],
        expected_code=400,
        method="PATCH",
    )

    assert (
        "new email can not be same as old one" in res_err_same["data"]["msg"]
    )

    res_err_existing = await wrap_httpx(
        api,
        url=URL,
        data={
            "email": res_register["payload"]["email"],
            "cbc_hmac_token": res_tk["cbc_hmac_token"],
        },
        access_token=res_tk["access_token"],
        expected_code=409,
        method="PATCH",
    )

    assert (
        "user with this email already exists"
        in res_err_existing["data"]["msg"]
    )
