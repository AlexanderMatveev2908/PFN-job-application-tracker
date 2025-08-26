import pytest
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib, login_ok_lib, register_ok_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

URL = "/user/delete-account?cbc_hmac_token="


@pytest.mark.asyncio
async def test_delete_account_ok(api) -> None:
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

    assert "account deleted" in res_delete["data"]["msg"].lower()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("invalid_cbc", 401, "cbc_hmac_invalid"),
        ("expired_jwt", 401, "jwt_expired"),
        ("expired_cbc", 401, "cbc_hmac_expired"),
        ("wrong_type", 401, "cbc_hmac_wrong_type"),
    ],
)
async def test_delete_account_invalid_cases(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    payload_url = ""
    access_token = ""

    if case == "invalid_cbc":
        res_tokens = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)
        payload_url = URL + res_tokens["cbc_hmac_token"][:-4] + "af90"
        access_token = res_tokens["access_token"]

    elif case == "expired_jwt":
        res_tokens = await get_tokens_lib(
            api, reverse=True, cbc_hmac_t=TokenT.MANAGE_ACC
        )
        payload_url = URL + res_tokens["cbc_hmac_token"]
        access_token = res_tokens["access_token"]

    elif case == "expired_cbc":
        res_tokens = await get_tokens_lib(
            api, reverse=True, cbc_hmac_t=TokenT.MANAGE_ACC
        )
        res_login = await login_ok_lib(
            api, register_payload=res_tokens["payload"]
        )
        payload_url = URL + res_tokens["cbc_hmac_token"]
        access_token = res_login["access_token"]

    elif case == "wrong_type":
        res_tokens = await get_tokens_lib(api)
        payload_url = URL + res_tokens["cbc_hmac_token"]
        access_token = res_tokens["access_token"]

    res = await wrap_httpx(
        api,
        url=payload_url,
        expected_code=expected_code,
        access_token=access_token,
        method="DELETE",
    )

    assert expected_msg in res["data"]["msg"].lower()
