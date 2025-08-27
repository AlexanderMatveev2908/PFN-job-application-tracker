import os
import pytest
from src.constants.reg import REG_CBC_HMAC
from src.lib.etc import grab
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

from tests.conf.lib.login import make_flow_log
from tests.conf.lib.register import register_ok_lib

URL = "/user/change-email"


@pytest.mark.asyncio
async def ok_t(api) -> None:
    res_register = await register_ok_lib(api)

    res_manage = await wrap_httpx(
        api,
        url="/user/manage-account",
        data={"password": res_register["payload"]["password"]},
        access_token=res_register["access_token"],
        expected_code=200,
    )
    assert REG_CBC_HMAC.fullmatch(grab(res_manage, "cbc_hmac_token"))

    new_email = os.urandom(20).hex() + "@gmail.com"

    res_mail = await wrap_httpx(
        api,
        url=URL,
        data={
            "email": new_email,
            "cbc_hmac_token": grab(res_manage, "cbc_hmac_token"),
        },
        access_token=res_register["access_token"],
        expected_code=200,
        method="PATCH",
    )

    assrt_msg(res_mail, "email sent to new address")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("invalid_jwt", 401, "jwt_invalid"),
        ("invalid_cbc", 401, "cbc_hmac_invalid"),
        ("expired_jwt", 401, "jwt_expired"),
        ("expired_cbc", 401, "cbc_hmac_expired"),
        ("same_email", 400, "new email can not be same as old one"),
        ("existing_email", 409, "user with this email already exists"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    payload = None
    access_token = ""
    method = "PATCH"

    if case == "invalid_jwt":
        res_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)
        payload = {
            "email": res_tk["payload"]["email"],
            "cbc_hmac_token": res_tk["cbc_hmac_token"],
        }
        access_token = res_tk["access_token"][:-4] + "abcd"

    elif case == "invalid_cbc":
        res_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)
        payload = {
            "email": res_tk["payload"]["email"],
            "cbc_hmac_token": res_tk["cbc_hmac_token"][:-4] + "abcd",
        }
        access_token = res_tk["access_token"]

    elif case == "expired_jwt":
        expired_tk = await get_tokens_lib(
            api, cbc_hmac_t=TokenT.MANAGE_ACC, reverse=True
        )
        payload = {
            "email": expired_tk["payload"]["email"],
            "cbc_hmac_token": expired_tk["cbc_hmac_token"],
        }
        access_token = expired_tk["access_token"]

    elif case == "expired_cbc":
        expired_tk = await get_tokens_lib(
            api, cbc_hmac_t=TokenT.MANAGE_ACC, reverse=True
        )
        res_login = await make_flow_log(
            api, register_payload=expired_tk["payload"]
        )
        payload = {
            "email": expired_tk["payload"]["email"],
            "cbc_hmac_token": expired_tk["cbc_hmac_token"],
        }
        access_token = res_login["access_token"]

    elif case == "same_email":
        res_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)
        payload = {
            "email": res_tk["payload"]["email"],
            "cbc_hmac_token": res_tk["cbc_hmac_token"],
        }
        access_token = res_tk["access_token"]

    elif case == "existing_email":
        res_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)
        res_register = await register_ok_lib(api)
        payload = {
            "email": res_register["payload"]["email"],
            "cbc_hmac_token": res_tk["cbc_hmac_token"],
        }
        access_token = res_tk["access_token"]

    res = await wrap_httpx(
        api,
        url=URL,
        data=payload,
        access_token=access_token,
        expected_code=expected_code,
        method=method,
    )

    assrt_msg(res, expected_msg)
