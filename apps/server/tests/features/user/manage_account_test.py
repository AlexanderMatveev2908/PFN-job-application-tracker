import pytest
from src.constants.reg import REG_CBC_HMAC
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

from tests.conf.lib.register import register_ok_lib

URL = "/user/manage-account"


@pytest.mark.asyncio
async def ok_t(api) -> None:
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
        ("jwt_expired", 401, "jwt_expired"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:

    res_tokens = await get_tokens_lib(api, expired=case.split("_expired"))
    pwd = res_tokens["payload"]["password"]

    res = await wrap_httpx(
        api,
        url=URL,
        data={
            "password": pwd + "wrong" if case == "invalid_password" else pwd
        },
        access_token=res_tokens["access_token"],
        expected_code=expected_code,
    )

    assrt_msg(res, expected_msg)
