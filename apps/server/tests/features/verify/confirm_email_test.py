import pytest
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg, assrt_sessions_tokens
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

URL = "/verify/confirm-email?cbc_hmac_token="


@pytest.mark.asyncio
async def ok_t(api) -> None:
    res_register = await get_tokens_lib(api)

    res_conf = await wrap_httpx(
        api,
        method="GET",
        url=f'{URL}{res_register["cbc_hmac_token"]}',
        expected_code=200,
    )

    assrt_sessions_tokens(res_conf)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("already_verified", 409, "user already verified"),
        ("cbc_hmac_expired", 401, "cbc_hmac_expired"),
        ("invalid", 401, "cbc_hmac_invalid"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:

    res_tokens = await get_tokens_lib(
        api,
        verify_user=case == "already_verified",
        cbc_hmac_t=TokenT.CONF_EMAIL,
        expired=case.split("_expired"),
    )
    cbc = res_tokens["cbc_hmac_token"]
    cbc = cbc[:-4] + "aaff" if case == "invalid" else cbc

    res_conf = await wrap_httpx(
        api, method="GET", url=f"{URL}{cbc}", expected_code=expected_code
    )

    assrt_msg(res_conf, expected_msg)
