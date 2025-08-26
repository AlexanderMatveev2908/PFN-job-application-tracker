from typing import Literal, TypedDict
from urllib.parse import urlencode
from httpx import AsyncClient
from src.__dev_only.payloads import RegisterPayloadT, get_payload_register
from src.constants.reg import (
    REG_CBC_HMAC,
    REG_ID,
    REG_JWE,
    REG_JWT,
    REG_SECRET_TOTP,
)
from src.models.token import TokenT
from src.models.user import UserDcT
from tests.conf.lib.data_structure import extract_login_payload
from tests.conf.lib.idx import wrap_httpx


class LoginOkReturnT(TypedDict):
    access_token: str
    refresh_token: str


class RegisterOkLibReturnT(LoginOkReturnT):
    payload: RegisterPayloadT


class SuccessReqTokensReturnT(RegisterOkLibReturnT):
    user: UserDcT
    cbc_hmac_token: str


class GetUser2FAReturnT(SuccessReqTokensReturnT):
    totp_secret: str
    backup_codes: list[str]


async def register_ok_lib(api) -> RegisterOkLibReturnT:
    payload = get_payload_register()

    res_register = await wrap_httpx(
        api,
        url="/auth/register",
        data=payload,
        expected_code=201,
    )

    assert REG_JWT.fullmatch(res_register["data"]["access_token"])
    assert REG_JWE.fullmatch(res_register["refresh_token"])

    return {
        "payload": payload,
        "access_token": res_register["data"]["access_token"],
        "refresh_token": res_register["refresh_token"],
    }


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


TokenArgT = Literal["jwt", "jwe", "cbc_hmac"]


async def get_tokens_lib(
    api: AsyncClient,
    reverse: bool = False,
    cbc_hmac_t: TokenT = TokenT.CONF_EMAIL,
    existing_payload: RegisterPayloadT | None = None,
    expired: list[TokenArgT] = [],
    verify_user: bool = False,
) -> SuccessReqTokensReturnT:
    payload = existing_payload or get_payload_register()

    if reverse:
        expired = ["jwt", "jwe", "cbc_hmac"]

    params: dict = {
        "cbc_hmac_token_t": cbc_hmac_t.value,
        "expired": expired,
        "verify_user": verify_user,
    }

    res_tokens = await wrap_httpx(
        api,
        url=f"/test/tokens-health?{urlencode(params, doseq=True)}",  # noqa: E501
        data=payload,
        expected_code=200,
    )

    assert REG_JWT.fullmatch(res_tokens["data"]["access_token"])
    assert REG_JWE.fullmatch(res_tokens["refresh_token"])
    assert REG_CBC_HMAC.fullmatch(res_tokens["data"]["cbc_hmac_token"])
    assert REG_ID.fullmatch(res_tokens["data"]["user"]["id"])

    if verify_user:
        assert res_tokens["data"]["user"]["is_verified"]

    return {
        "user": res_tokens["data"]["user"],
        "access_token": res_tokens["data"]["access_token"],
        "refresh_token": res_tokens["refresh_token"],
        "cbc_hmac_token": res_tokens["data"]["cbc_hmac_token"],
        "payload": payload,
    }


async def get_verified_user_lib(
    api: AsyncClient,
    token_t: TokenT = TokenT.MANAGE_ACC,
    expired: list[TokenArgT] = [],
    existing_payload: RegisterPayloadT | None = None,
) -> SuccessReqTokensReturnT:

    res = await get_tokens_lib(
        api,
        cbc_hmac_t=token_t,
        expired=expired,
        verify_user=True,
        existing_payload=existing_payload,
    )

    return res


async def get_us_2FA(
    api: AsyncClient,
) -> GetUser2FAReturnT:
    res_us = await get_verified_user_lib(
        api,
    )

    res_2FA = await wrap_httpx(
        api,
        url="/user/2FA",
        method="PATCH",
        access_token=res_us["access_token"],
        data={"cbc_hmac_token": res_us["cbc_hmac_token"]},
        expected_code=200,
    )

    assert REG_SECRET_TOTP.fullmatch(res_2FA["data"]["totp_secret"])

    assert len(res_2FA["data"]["backup_codes"]) == 8

    return {
        **res_us,
        "totp_secret": res_2FA["data"]["totp_secret"],
        "backup_codes": res_2FA["data"]["backup_codes"],
    }
