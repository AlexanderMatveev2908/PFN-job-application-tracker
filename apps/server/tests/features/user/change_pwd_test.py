import os
from httpx import AsyncClient
import pytest

from src.constants.reg import REG_CBC_HMAC
from src.models.token import TokenT
from tests.conf.lib.data_structure import extract_login_payload
from tests.conf.lib.etc import get_tokens_lib, register_ok_lib
from tests.conf.lib.idx import wrap_httpx

URL_MNG = "/user/manage-account"
URL_CHG = "/user/change-pwd"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_manage = await wrap_httpx(
        api,
        url=URL_MNG,
        access_token=res_register["access_token"],
        data={"password": res_register["payload"]["password"]},
        expected_code=200,
    )

    assert REG_CBC_HMAC.fullmatch(res_manage["data"]["cbc_hmac_token"])

    res_change = await wrap_httpx(
        api,
        url=URL_CHG,
        expected_code=200,
        data={
            "password": res_register["payload"]["password"]
            + (os.urandom(5).hex()),
            "cbc_hmac_token": res_manage["data"]["cbc_hmac_token"],
        },
        access_token=res_register["access_token"],
        method="PATCH",
    )

    assert "password updated" in res_change["data"]["msg"]


@pytest.mark.asyncio
async def err_same_t(api: AsyncClient) -> None:
    res_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)

    err_res = await wrap_httpx(
        api,
        url=URL_CHG,
        access_token=res_tk["access_token"],
        data={
            "cbc_hmac_token": res_tk["cbc_hmac_token"],
            "password": res_tk["payload"]["password"],
        },
        method="PATCH",
        expected_code=400,
    )

    assert (
        "new password must be different from old one" in err_res["data"]["msg"]
    )


@pytest.mark.asyncio
async def invalid_token_t(api: AsyncClient) -> None:
    res_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)

    err_res = await wrap_httpx(
        api,
        url=URL_CHG,
        access_token=res_tk["access_token"],
        data={
            "cbc_hmac_token": "abcd" + res_tk["cbc_hmac_token"][4:],
            "password": res_tk["payload"]["password"],
        },
        method="PATCH",
        expected_code=401,
    )

    assert "CBC_HMAC_INVALID" in err_res["data"]["msg"]


@pytest.mark.asyncio
async def access_expired_tk_t(api: AsyncClient) -> None:
    res_expired = await get_tokens_lib(
        api, cbc_hmac_t=TokenT.MANAGE_ACC, reverse=True
    )

    err_res = await wrap_httpx(
        api,
        url=URL_CHG,
        access_token=res_expired["access_token"],
        data={
            "cbc_hmac_token": res_expired["cbc_hmac_token"],
            "password": res_expired["payload"]["password"],
        },
        method="PATCH",
        expected_code=401,
    )

    assert "ACCESS_TOKEN_EXPIRED" in err_res["data"]["msg"]


@pytest.mark.asyncio
async def cbc_expired_t(api: AsyncClient) -> None:
    res_expired = await get_tokens_lib(
        api, cbc_hmac_t=TokenT.MANAGE_ACC, reverse=True
    )

    login_res = await wrap_httpx(
        api,
        url="/auth/login",
        data=extract_login_payload(res_expired["payload"]),
        expected_code=200,
    )

    err_res = await wrap_httpx(
        api,
        url=URL_CHG,
        access_token=login_res["data"]["access_token"],
        data={
            "cbc_hmac_token": res_expired["cbc_hmac_token"],
            "password": res_expired["payload"]["password"],
        },
        method="PATCH",
        expected_code=401,
    )

    assert "CBC_HMAC_EXPIRED" in err_res["data"]["msg"]
