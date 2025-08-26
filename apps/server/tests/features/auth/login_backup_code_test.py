from httpx import AsyncClient
import pytest

from src.constants.reg import REG_CBC_HMAC, REG_JWT
from tests.conf.lib.data_structure import extract_login_payload
from tests.conf.lib.get_us import get_us_2FA
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_us_2fa = await get_us_2FA(
        api,
    )

    res_login = await wrap_httpx(
        api,
        url="/auth/login",
        data=extract_login_payload(res_us_2fa["payload"]),
        expected_code=200,
    )

    assert REG_CBC_HMAC.fullmatch(res_login["data"]["cbc_hmac_token"])

    res_login_2fa = await wrap_httpx(
        api,
        url="/auth/login-2FA-backup-code",
        expected_code=200,
        data={
            "cbc_hmac_token": res_login["data"]["cbc_hmac_token"],
            "backup_code": res_us_2fa["backup_codes"][0],
        },
    )

    assert REG_JWT.fullmatch(res_login_2fa["data"]["access_token"])
    assert res_login_2fa["data"]["backup_codes_left"] == 7


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("wrong_code", 401, "backup_code_invalid"),
        # ("finished_codes", 401, "user has no backup codes"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    res_us_2fa = await get_us_2FA(api)

    if case == "finished_codes":
        for i in range(8):
            res_login = await wrap_httpx(
                api,
                url="/auth/login",
                data=extract_login_payload(res_us_2fa["payload"]),
                expected_code=200,
            )

            code = res_us_2fa["backup_codes"][i]

            res_login_2fa = await wrap_httpx(
                api,
                url="/auth/login-2FA-backup-code",
                expected_code=200,
                data={
                    "cbc_hmac_token": res_login["data"]["cbc_hmac_token"],
                    "backup_code": (code),
                },
            )

            assert REG_JWT.fullmatch(res_login_2fa["data"]["access_token"])

    res_login = await wrap_httpx(
        api,
        url="/auth/login",
        data=extract_login_payload(res_us_2fa["payload"]),
        expected_code=200,
    )

    totp_code = res_us_2fa["backup_codes"][-1]

    res_login_2fa = await wrap_httpx(
        api,
        url="/auth/login-2FA-backup-code",
        expected_code=expected_code,
        data={
            "cbc_hmac_token": res_login["data"]["cbc_hmac_token"],
            "backup_code": (
                totp_code[:-2] + "12" if case == "wrong_code" else totp_code
            ),
        },
    )

    assert expected_msg in res_login_2fa["data"]["msg"].lower()
