import os
import pytest
from src.constants.reg import REG_CBC_HMAC
from src.lib.etc import grab
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg, extract_login_payload
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

from tests.conf.lib.register import register_ok_lib

URL_MNG = "/user/manage-account"
URL_CHG = "/user/change-pwd"


@pytest.mark.asyncio
async def ok_t(api) -> None:
    res_register = await register_ok_lib(api)

    res_manage = await wrap_httpx(
        api,
        url=URL_MNG,
        access_token=res_register["access_token"],
        data={"password": res_register["payload"]["password"]},
        expected_code=200,
    )
    assert REG_CBC_HMAC.fullmatch(grab(res_manage, "cbc_hmac_token"))

    new_pwd = res_register["payload"]["password"] + os.urandom(5).hex()

    res_change = await wrap_httpx(
        api,
        url=URL_CHG,
        expected_code=200,
        data={
            "password": new_pwd,
            "cbc_hmac_token": grab(res_manage, "cbc_hmac_token"),
        },
        access_token=res_register["access_token"],
        method="PATCH",
    )

    assrt_msg(res_change, "password updated")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("same_pwd", 400, "new password must be different from old one"),
        ("invalid_cbc", 401, "cbc_hmac_invalid"),
        ("expired_access", 401, "jwt_expired"),
        ("expired_cbc", 401, "cbc_hmac_expired"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    payload = {}
    access_token = ""
    method = "PATCH"

    if case == "same_pwd":
        res_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)
        payload = {
            "cbc_hmac_token": res_tk["cbc_hmac_token"],
            "password": res_tk["payload"]["password"],
        }
        access_token = res_tk["access_token"]

    elif case == "invalid_cbc":
        res_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)
        payload = {
            "cbc_hmac_token": "abcd" + res_tk["cbc_hmac_token"][4:],
            "password": res_tk["payload"]["password"],
        }
        access_token = res_tk["access_token"]

    elif case == "expired_access":
        res_expired = await get_tokens_lib(
            api, cbc_hmac_t=TokenT.MANAGE_ACC, reverse=True
        )
        payload = {
            "cbc_hmac_token": res_expired["cbc_hmac_token"],
            "password": res_expired["payload"]["password"],
        }
        access_token = res_expired["access_token"]

    elif case == "expired_cbc":
        res_expired = await get_tokens_lib(
            api, cbc_hmac_t=TokenT.MANAGE_ACC, reverse=True
        )
        login_res = await wrap_httpx(
            api,
            url="/auth/login",
            data=extract_login_payload(res_expired["payload"]),
            expected_code=200,
        )
        payload = {
            "cbc_hmac_token": res_expired["cbc_hmac_token"],
            "password": res_expired["payload"]["password"],
        }
        access_token = grab(login_res, "access_token")

    res = await wrap_httpx(
        api,
        url=URL_CHG,
        data=payload,
        access_token=access_token,
        expected_code=expected_code,
        method=method,
    )
    assrt_msg(res, expected_msg)
