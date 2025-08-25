from typing import TypedDict, cast
from httpx import AsyncClient
from src.__dev_only.payloads import RegisterPayloadT, get_payload_register
from src.constants.reg import REG_CBC_HMAC, REG_JWE, REG_JWT
from src.models.token import TokenT
from tests.conf.lib.data_structure import extract_login_payload
from tests.conf.lib.idx import wrap_httpx


class SuccessReqTokensReturnT(TypedDict):
    access_token: str
    refresh_token: str
    cbc_hmac_token: str
    payload: RegisterPayloadT


async def register_ok_lib(api) -> SuccessReqTokensReturnT:
    payload = get_payload_register()

    res_register = await wrap_httpx(
        api,
        url="/auth/register",
        data=payload,
        expected_code=201,
    )

    assert REG_JWT.fullmatch(res_register["data"]["access_token"])
    assert REG_JWE.fullmatch(res_register["refresh_token"])

    return cast(
        SuccessReqTokensReturnT, {"payload": payload, **res_register["data"]}
    )


class LoginOkReturnT(TypedDict):
    access_token: str


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

    return {"access_token": res_login["data"]["access_token"]}


async def get_tokens_lib(
    api: AsyncClient,
    reverse: bool = False,
    cbc_hmac_t: TokenT = TokenT.CONF_EMAIL,
    existing_payload: RegisterPayloadT | None = None,
) -> SuccessReqTokensReturnT:
    payload = existing_payload or get_payload_register()

    res_register = await wrap_httpx(
        api,
        url=f"/test/{'get-tokens-expired' if reverse else 'tokens-health'}?cbc_hmac_token_t={cbc_hmac_t.value}",  # noqa: E501
        data=payload,
        expected_code=200,
    )

    assert REG_JWT.fullmatch(res_register["data"]["access_token"])
    assert REG_JWE.fullmatch(res_register["refresh_token"])
    assert REG_CBC_HMAC.fullmatch(res_register["data"]["cbc_hmac_token"])

    return {
        "access_token": res_register["data"]["access_token"],
        "refresh_token": res_register["refresh_token"],
        "cbc_hmac_token": res_register["data"]["cbc_hmac_token"],
        "payload": payload,
    }
