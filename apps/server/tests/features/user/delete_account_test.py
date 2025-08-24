from httpx import AsyncClient
import pytest

from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib, login_ok_lib, register_ok_lib
from tests.conf.lib.idx import wrap_httpx

URL = "/user/delete-account?cbc_hmac_token="


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_manage = await wrap_httpx(
        api,
        url="/user/manage-account",
        access_token=res_register["access_token"],
        expected_code=200,
        data={"password": res_register["payload"]["password"]},
    )

    res_delete = await wrap_httpx(
        api,
        url=URL + res_manage["data"]["cbc_hmac_token"],
        method="DELETE",
        access_token=res_register["access_token"],
        expected_code=200,
    )

    assert "account deleted" in res_delete["data"]["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)

    res_del = await wrap_httpx(
        api,
        url=f'{URL}{res_tokens["cbc_hmac_token"][:-4]+'af90'}',
        expected_code=401,
        access_token=res_tokens["access_token"],
        method="DELETE",
    )

    assert "CBC_HMAC_INVALID" in res_del["data"]["msg"]


@pytest.mark.asyncio
async def err_expired_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(
        api, reverse=True, cbc_hmac_t=TokenT.MANAGE_ACC
    )

    err_jwt = await wrap_httpx(
        api,
        url=f'{URL}{res_tokens["cbc_hmac_token"]}',
        expected_code=401,
        access_token=res_tokens["access_token"],
        method="DELETE",
    )

    assert "ACCESS_TOKEN_EXPIRED" in err_jwt["data"]["msg"]

    res_login = await login_ok_lib(api, register_payload=res_tokens["payload"])

    err_cbc = await wrap_httpx(
        api,
        url=f'{URL}{res_tokens["cbc_hmac_token"]}',
        expected_code=401,
        access_token=res_login["access_token"],
        method="DELETE",
    )

    assert "CBC_HMAC_EXPIRED" in err_cbc["data"]["msg"]


@pytest.mark.asyncio
async def wrong_act_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(api)

    err_type = await wrap_httpx(
        api,
        url=f'{URL}{res_tokens["cbc_hmac_token"]}',
        expected_code=401,
        access_token=res_tokens["access_token"],
        method="DELETE",
    )

    assert "CBC_HMAC_WRONG_TYPE" in err_type["data"]["msg"]
