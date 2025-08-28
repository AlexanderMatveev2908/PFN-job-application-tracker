import pytest
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient
from tests.conf.lib.register import register_ok_lib

URL = "/user/delete-account?cbc_hmac_token="


@pytest.mark.asyncio
async def ok_t(api) -> None:
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

    assrt_msg(res_delete, "account deleted")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("invalid_cbc", 401, "cbc_hmac_invalid"),
        ("jwt_expired", 401, "jwt_expired"),
        ("cbc_hmac_expired", 401, "cbc_hmac_expired"),
        ("wrong_type", 401, "cbc_hmac_wrong_type"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:

    res_tokens = await get_tokens_lib(
        api,
        cbc_hmac_t=(
            TokenT.CONF_EMAIL if case == "wrong_type" else TokenT.MANAGE_ACC
        ),
        expired=case.split("_expired"),
    )
    cbc_hmac = res_tokens["cbc_hmac_token"]
    payload_url = URL + (
        cbc_hmac[:-4] + "aaff" if case == "invalid_cbc" else cbc_hmac
    )

    res = await wrap_httpx(
        api,
        url=payload_url,
        expected_code=expected_code,
        access_token=res_tokens["access_token"],
        method="DELETE",
    )

    assrt_msg(res, expected_msg)
