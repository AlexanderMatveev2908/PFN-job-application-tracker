import pytest
from src.constants.reg import REG_CBC_HMAC
from tests.conf.lib.etc import get_tokens_lib, register_ok_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

URL = "/user/manage-account"


@pytest.mark.asyncio
async def test_manage_account_ok(api) -> None:
    res_register = await register_ok_lib(api)

    res_manage = await wrap_httpx(
        api,
        url=URL,
        data={"password": res_register["payload"]["password"]},
        access_token=res_register["access_token"],
        expected_code=200,
    )

    assert REG_CBC_HMAC.fullmatch(res_manage["data"]["cbc_hmac_token"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("invalid_password", 401, "invalid password"),
        ("expired_access", 401, "access_token_expired"),
    ],
)
async def test_manage_account_invalid_cases(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    payload = {}
    access_token = ""

    if case == "invalid_password":
        res_register = await register_ok_lib(api)
        payload = {"password": res_register["payload"]["password"][4:]}
        access_token = res_register["access_token"]

    elif case == "expired_access":
        res_tokens = await get_tokens_lib(api, reverse=True)
        payload = {"password": res_tokens["payload"]["password"]}
        access_token = res_tokens["access_token"]

    res = await wrap_httpx(
        api,
        url=URL,
        data=payload,
        access_token=access_token,
        expected_code=expected_code,
    )

    assert expected_msg in res["data"]["msg"].lower()
