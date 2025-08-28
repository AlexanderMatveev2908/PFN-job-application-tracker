import pytest
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

URL = "/verify/recover-pwd?cbc_hmac_token="


@pytest.mark.asyncio
async def ok_t(api) -> None:
    res_tokens = await get_tokens_lib(api, cbc_hmac_t=TokenT.RECOVER_PWD)

    res_check = await wrap_httpx(
        api,
        url=f'{URL}{res_tokens["cbc_hmac_token"]}',
        expected_code=200,
        method="GET",
    )

    assrt_msg(res_check, "verification successful")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("not_provided", 401, "cbc_hmac_not_provided"),
        ("invalid_format", 401, "cbc_hmac_invalid_format"),
        ("wrong_type", 401, "cbc_hmac_wrong_type"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:

    res_tokens = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT[
            "CONF_EMAIL" if case == "wrong_type" else "RECOVER_PWD"
        ],
    )
    cbc = res_tokens["cbc_hmac_token"]

    if case == "not_provided":
        cbc = ""
    elif case == "invalid_format":
        cbc += "12345"

    res_check = await wrap_httpx(
        api,
        url=f"{URL}{cbc}",
        expected_code=expected_code,
        method="GET",
    )

    assrt_msg(res_check, expected_msg)
