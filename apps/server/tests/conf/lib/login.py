from httpx import AsyncClient
from src.__dev_only.payloads import RegisterPayloadT
from src.models.token import TokenT
from tests.conf.lib.data_structure import (
    assrt_sessions_tokens,
    gen_totp,
    get_aad_cbc_hmac,
    extract_login_payload,
)
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.get_us import make_setup_2FA
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.types import User2FAReturnT, LoginOkReturnT


async def make_flow_log(
    api: AsyncClient, register_payload: RegisterPayloadT
) -> LoginOkReturnT:

    res_login = await wrap_httpx(
        api,
        url="/auth/login",
        data=extract_login_payload(register_payload),
        expected_code=200,
    )

    assrt_sessions_tokens(res_login)

    return {
        "access_token": res_login["data"]["access_token"],
        "refresh_token": res_login["refresh_token"],
    }


async def make_flow_log_2FA(
    api: AsyncClient, cbc_hmac_t: TokenT = TokenT.MANAGE_ACC_2FA
) -> User2FAReturnT:
    res_us_2fa: User2FAReturnT = await make_setup_2FA(api)

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
        url="/auth/login-2FA",
        data={
            "totp_code": gen_totp(res_us_2fa["totp_secret"]),
            "cbc_hmac_token": login_token,
        },
        expected_code=200,
    )

    assrt_sessions_tokens(res_login_2fa)

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
