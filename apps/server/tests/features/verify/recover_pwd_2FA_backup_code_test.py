from httpx import AsyncClient
import pytest
from src.lib.pwd_gen import gen_pwd
from src.models.token import TokenT
from tests.conf.lib.data_structure import (
    assrt_msg,
    assrt_sessions_tokens,
)
from tests.conf.lib.get_us import get_us_2FA_lib
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_logged = await get_us_2FA_lib(api, cbc_hmac_t=TokenT.RECOVER_PWD)

    await wrap_httpx(
        api,
        url=f"/verify/recover-pwd?cbc_hmac_token={res_logged['cbc_hmac_token']}",  # noqa: E501
        expected_code=200,
        method="GET",
    )

    res_2FA = await wrap_httpx(
        api,
        url="/verify/recover-pwd-2FA",
        expected_code=200,
        data={
            "cbc_hmac_token": res_logged["cbc_hmac_token"],
            "backup_code": res_logged["backup_codes"][0],
        },
    )

    res_new_pwd = await wrap_httpx(
        api,
        url="/auth/recover-pwd-2FA",
        data={
            "password": gen_pwd(5),
            "cbc_hmac_token": res_2FA["data"]["cbc_hmac_token"],
        },
        method="PATCH",
    )

    assrt_sessions_tokens(res_new_pwd)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("wrong_code", 401, "backup_code_invalid"),
        ("wrong_endpoint", 403, "user must follow 2fa flow"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    res_2fa = await get_us_2FA_lib(
        api,
        cbc_hmac_t=TokenT.RECOVER_PWD,
    )

    if case == "wrong_endpoint":
        res_change = await wrap_httpx(
            api,
            url="/auth/recover-pwd",
            data={
                "password": gen_pwd(5),
                "cbc_hmac_token": res_2fa["cbc_hmac_token"],
            },
            method="PATCH",
            expected_code=expected_code,
        )

        assrt_msg(res_change, expected_msg)
        return

    await wrap_httpx(
        api,
        url=f'/verify/recover-pwd?cbc_hmac_token={res_2fa["cbc_hmac_token"]}',
        method="GET",
        expected_code=200,
    )

    res_backup = await wrap_httpx(
        api,
        url="/verify/recover-pwd-2FA",
        expected_code=expected_code,
        data={
            "cbc_hmac_token": res_2fa["cbc_hmac_token"],
            "backup_code": (
                "1234-5678"
                if case == "wrong_code"
                else res_2fa["backup_codes"][0]
            ),
        },
    )

    assrt_msg(res_backup, expected_msg)
