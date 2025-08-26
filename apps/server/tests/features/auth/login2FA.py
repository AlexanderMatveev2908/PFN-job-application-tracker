from httpx import AsyncClient
import pyotp
import pytest

from src.constants.reg import REG_CBC_HMAC, REG_JWE, REG_JWT
from src.lib.data_structure import b_to_d, h_to_b
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib, get_user_2FA
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_2FA = await get_user_2FA(api)

    res_login = await wrap_httpx(
        api,
        url="/auth/login",
        data={
            "email": res_2FA["payload"]["email"],
            "password": res_2FA["payload"]["password"],
        },
        expected_code=200,
    )

    cbc_hmac_token: str = res_login["data"]["cbc_hmac_token"]

    assert REG_CBC_HMAC.fullmatch(cbc_hmac_token)
    assert (
        TokenT(b_to_d(h_to_b(cbc_hmac_token.split(".")[0]))["token_t"])
        == TokenT.LOGIN_2FA
    )

    res_login_totp = await wrap_httpx(
        api,
        url="/auth/login-totp",
        data={
            "totp_code": pyotp.TOTP(res_2FA["totp_secret"]).now(),
            "cbc_hmac_token": res_login["data"]["cbc_hmac_token"],
        },
        expected_code=200,
    )

    assert REG_JWT.fullmatch(res_login_totp["data"]["access_token"])
    assert REG_JWE.fullmatch(res_login_totp["refresh_token"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [("cbc_hmac_expired", 401, "cbc_hmac_expired")],
)
async def base_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    res_us_2FA = await get_user_2FA(api)

    res_tokens = await get_tokens_lib(
        api,
        existing_payload=res_us_2FA["payload"],
        expired=case.split("_expired") if case.endswith("_expired") else [],
        cbc_hmac_t=TokenT.LOGIN_2FA,
    )

    res_totp = await wrap_httpx(
        api,
        url="/auth/login-totp",
        data={
            "totp_code": pyotp.TOTP(res_us_2FA["totp_secret"]).now(),
            "cbc_hmac_token": res_tokens["cbc_hmac_token"],
        },
        expected_code=expected_code,
    )

    assert expected_msg in res_totp["data"]["msg"].lower()
