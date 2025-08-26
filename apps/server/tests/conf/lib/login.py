from httpx import AsyncClient
import pyotp
from src.__dev_only.payloads import RegisterPayloadT
from src.constants.reg import REG_CBC_HMAC, REG_JWE, REG_JWT
from src.lib.data_structure import b_to_d, h_to_b
from src.models.token import TokenT
from tests.conf.lib.data_structure import extract_login_payload
from tests.conf.lib.etc import get_us_2FA
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.types import GetUser2FAReturnT, LoginOkReturnT


async def login_ok_lib(
    api: AsyncClient, register_payload: RegisterPayloadT
) -> LoginOkReturnT:

    res_login = await wrap_httpx(
        api,
        url="/auth/login",
        data=extract_login_payload(register_payload),
        expected_code=200,
    )

    assert REG_JWE.fullmatch(res_login["refresh_token"])
    assert REG_JWT.fullmatch(res_login["data"]["access_token"])

    return {
        "access_token": res_login["data"]["access_token"],
        "refresh_token": res_login["refresh_token"],
    }


async def get_logged_2fa(api: AsyncClient) -> GetUser2FAReturnT:
    res_us_2fa: GetUser2FAReturnT = await get_us_2FA(api)

    res_login = await wrap_httpx(
        api,
        url="/auth/login-totop",
        data=extract_login_payload(res_us_2fa["payload"]),
        expected_code=200,
    )

    assert REG_CBC_HMAC.fullmatch(res_login["data"]["cbc_hmac_token"])
    assert (
        TokenT(
            b_to_d(h_to_b(res_login["data"]["cbc_hmac_token"].split(".")[0]))[
                "token_t"
            ]
        )
        == TokenT.LOGIN_2FA
    )

    res_login_2fa = await wrap_httpx(
        api,
        url="/auth/lgoin-totp",
        data={"totp_code": pyotp.TOTP(res_us_2fa["totp_secret"]).now()},
        expected_code=200,
    )

    assert REG_JWT.fullmatch(res_login_2fa["data"]["access_token"])
    assert REG_JWE.fullmatch(res_login_2fa["refresh_token"])

    return res_us_2fa
