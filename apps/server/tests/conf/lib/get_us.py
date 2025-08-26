from httpx import AsyncClient

from src.__dev_only.payloads import RegisterPayloadT
from src.constants.reg import REG_SECRET_TOTP
from src.models.token import TokenT
from tests.conf.lib.etc import TokenArgT, get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.types import GetUser2FAReturnT, SuccessReqTokensReturnT


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
