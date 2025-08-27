from typing import Literal
from urllib.parse import urlencode
from httpx import AsyncClient
from src.__dev_only.payloads import RegisterPayloadT, get_payload_register
from src.constants.reg import (
    REG_CBC_HMAC,
    REG_ID,
)
from src.lib.etc import grab
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_sessions_tokens
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.types import (
    SuccessReqTokensReturnT,
)


TokenArgT = Literal["jwt", "jwe", "cbc_hmac"]


async def get_tokens_lib(
    api: AsyncClient,
    reverse: bool = False,
    cbc_hmac_t: TokenT = TokenT.CONF_EMAIL,
    existing_payload: RegisterPayloadT | None = None,
    expired: list[TokenArgT] | list[str] = [],
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

    assrt_sessions_tokens(res_tokens)
    assert REG_CBC_HMAC.fullmatch(res_tokens["data"]["cbc_hmac_token"])
    assert REG_ID.fullmatch(res_tokens["data"]["user"]["id"])

    if verify_user:
        assert grab(res_tokens, "is_verified")

    return {
        "user": res_tokens["data"]["user"],
        "access_token": res_tokens["data"]["access_token"],
        "refresh_token": res_tokens["refresh_token"],
        "cbc_hmac_token": res_tokens["data"]["cbc_hmac_token"],
        "payload": payload,
    }
