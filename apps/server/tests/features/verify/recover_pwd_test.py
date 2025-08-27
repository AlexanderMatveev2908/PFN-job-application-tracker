import pytest
from src.models.token import TokenT
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

    assert "verification successful" in res_check["data"]["msg"].lower()


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
    url = ""

    if case == "not_provided":
        url = f"{URL}"

    elif case == "invalid_format":
        res_tokens = await get_tokens_lib(api, cbc_hmac_t=TokenT.RECOVER_PWD)
        url = f"{URL}{'hack' + res_tokens['cbc_hmac_token'][4:]}"

    elif case == "wrong_type":
        res_tokens = await get_tokens_lib(api, cbc_hmac_t=TokenT.CHANGE_PWD)
        url = f"{URL}{res_tokens['cbc_hmac_token']}"

    res_check = await wrap_httpx(
        api,
        url=url,
        expected_code=expected_code,
        method="GET",
    )

    assert expected_msg in res_check["data"]["msg"].lower()
