from typing import cast
from urllib.parse import urlencode
from httpx import AsyncClient

from src.__dev_only.payloads import RegisterPayloadT
from src.constants.reg import REG_CBC_HMAC, REG_SECRET_TOTP
from src.lib.etc import grab
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_sessions_tokens
from tests.conf.lib.etc import TokenArgT, get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.types import User2FAReturnT, SuccessReqTokensReturnT


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


async def make_setup_2FA(
    api: AsyncClient,
) -> User2FAReturnT:
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

    assert len(grab(res_2FA, "backup_codes")) == 8

    return {
        **res_us,
        "totp_secret": res_2FA["data"]["totp_secret"],
        "backup_codes": grab(res_2FA, "backup_codes"),
    }


async def get_us_2FA_lib(
    api: AsyncClient,
    cbc_hmac_t: TokenT = TokenT.MANAGE_ACC,
    empty_codes: bool = False,
    expired: list[TokenArgT] | list[str] = [],
) -> User2FAReturnT:
    params = {
        "cbc_hmac_t": cbc_hmac_t.value,
        "empty_codes": empty_codes,
        "expired": expired,
    }

    res = await wrap_httpx(
        api,
        url=f"/test/get-user-2FA?{urlencode(params, doseq=True)}",
        expected_code=200,
    )

    assrt_sessions_tokens(res)
    assert REG_CBC_HMAC.fullmatch(grab(res, "cbc_hmac_token"))
    assert len(res["data"]["backup_codes"]) == (0 if empty_codes else 8)

    assert REG_SECRET_TOTP.fullmatch(res["data"]["totp_secret"])

    return cast(
        User2FAReturnT,
        {**res["data"], "refresh_token": res["refresh_token"]},
    )
