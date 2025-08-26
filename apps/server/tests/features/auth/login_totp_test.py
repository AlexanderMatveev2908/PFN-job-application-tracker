from httpx import AsyncClient
import pyotp
import pytest
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.get_us import make_setup_2FA
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.login import make_flow_log_2FA


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    await make_flow_log_2FA(api)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("cbc_hmac_expired", 401, "cbc_hmac_expired"),
        ("totp_code_invalid", 401, "totp_code_invalid"),
        ("wrong_type", 401, "cbc_hmac_wrong_type"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    res_us_2FA = await make_setup_2FA(api)

    res_tokens = await get_tokens_lib(
        api,
        existing_payload=res_us_2FA["payload"],
        expired=case.split("_expired") if case.endswith("_expired") else [],
        cbc_hmac_t=(
            TokenT.CONF_EMAIL if case == "wrong_type" else TokenT.LOGIN_2FA
        ),
    )

    totp_code = pyotp.TOTP(res_us_2FA["totp_secret"]).now()

    res_totp = await wrap_httpx(
        api,
        url="/auth/login-2FA-totp",
        data={
            "totp_code": (
                totp_code[:-2] + "12"
                if case == "totp_code_invalid"
                else totp_code
            ),
            "cbc_hmac_token": res_tokens["cbc_hmac_token"],
        },
        expected_code=expected_code,
    )

    assert expected_msg in res_totp["data"]["msg"].lower()
