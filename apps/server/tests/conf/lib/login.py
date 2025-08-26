from httpx import AsyncClient
from src.__dev_only.payloads import RegisterPayloadT
from src.constants.reg import REG_JWE, REG_JWT
from src.models.token import TokenT
from tests.conf.lib.data_structure import (
    gen_totp,
    get_aad_cbc_hmac,
    extract_login_payload,
)
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.get_us import get_us_2FA
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


async def get_logged_2fa(
    api: AsyncClient, cbc_hmac_t: TokenT = TokenT.MANAGE_ACC_2FA
) -> GetUser2FAReturnT:
    res_us_2fa: GetUser2FAReturnT = await get_us_2FA(api)

    res_login = await wrap_httpx(
        api,
        url="/auth/login",
        data=extract_login_payload(res_us_2fa["payload"]),
        expected_code=200,
    )

    login_token = res_login["data"]["cbc_hmac_token"]
    get_aad_cbc_hmac(token=login_token, token_t=TokenT.LOGIN_2FA)

    res_login_2fa = await wrap_httpx(
        api,
        url="/auth/login-totp",
        data={
            "totp_code": gen_totp(res_us_2fa["totp_secret"]),
            "cbc_hmac_token": login_token,
        },
        expected_code=200,
    )

    assert REG_JWT.fullmatch(res_login_2fa["data"]["access_token"])
    assert REG_JWE.fullmatch(res_login_2fa["refresh_token"])

    res_tokens = await get_tokens_lib(
        api,
        cbc_hmac_t=cbc_hmac_t,
        existing_payload=res_us_2fa["payload"],
    )

    return {
        "backup_codes": res_us_2fa["backup_codes"],
        "totp_secret": res_us_2fa["totp_secret"],
        "user": res_us_2fa["user"],
        "payload": res_us_2fa["payload"],
        "access_token": res_tokens["access_token"],
        "refresh_token": res_tokens["refresh_token"],
        "cbc_hmac_token": res_tokens["cbc_hmac_token"],
    }
