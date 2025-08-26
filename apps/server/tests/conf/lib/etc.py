from typing import Literal
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
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.types import (
    GetUser2FAReturnT,
    SuccessReqTokensReturnT,
)


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
