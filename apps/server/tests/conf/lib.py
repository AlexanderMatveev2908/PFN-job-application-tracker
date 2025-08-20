from typing import Any, Literal, TypedDict, cast
from httpx import AsyncClient, Response

from src.constants.reg import REG_CBC_HMAC, REG_ID, REG_JWE, REG_JWT
from src.lib.logger import clg
from src.models.token import TokenT
from tests.conf.constants import RegisterPayloadT, get_payload_register


def parse_res(res: Response) -> dict:
    data = res.json()

    full = str(res.request.url)
    part = (
        full[full.index("/api/v1") + len("/api/v1") :]  # noqa: E203
    ).split("?", 1)[0]

    clg(
        data,
        ttl=f"💾 {part} — 🚦 {res.status_code}",
    )

    return data


class WrapReturnT(TypedDict):
    data: dict[Literal["msg"] | str, Any]
    refresh_token: str


async def wrap_httpx(
    api: AsyncClient,
    *,
    url: str,
    method: Literal["POST", "GET"] = "POST",
    data: Any | None = None,
    expected_code: int = 200,
) -> WrapReturnT:

    if method == "POST":
        res = await api.post(url, json=data)
    elif method == "GET":
        res = await api.get(url)

    parsed = parse_res(res)
    refresh = (
        res.cookies.get(
            "refresh_token",
        )
        or "N/A"
    )

    try:
        assert (
            res.status_code == expected_code
        ), f"❌ got {res.status_code} • expected {expected_code}"

    except Exception:
        raise

    return {
        "data": parsed,
        "refresh_token": refresh,
    }


def extract_login_payload(
    payload_register: RegisterPayloadT,
) -> dict[Literal["email", "password"], str]:
    return {
        "email": payload_register["email"],
        "password": payload_register["password"],
    }


class RegisterReturnT(TypedDict):
    access_token: str
    refresh_token: str
    cbc_hmac_token: str
    msg: str


class RegisterOkReturnT(TypedDict):
    payload: RegisterPayloadT
    data_register: RegisterReturnT


async def register_ok_lib(api) -> RegisterOkReturnT:
    payload = get_payload_register()

    res_register = await wrap_httpx(
        api,
        url="/auth/register",
        data=payload,
        expected_code=201,
    )

    assert REG_JWT.fullmatch(res_register["data"]["access_token"])
    assert REG_JWE.fullmatch(res_register["refresh_token"])
    assert REG_CBC_HMAC.fullmatch(res_register["data"]["cbc_hmac_token"])
    assert "new_user" in res_register["data"]

    return {
        "payload": payload,
        "data_register": cast(RegisterReturnT, res_register["data"]),
    }


class GenTokensReturnT(TypedDict):
    access_token: str
    refresh_token: str
    cbc_hmac_token: str
    payload: RegisterPayloadT


async def get_tokens_lib(
    api: AsyncClient,
    reverse: bool = False,
    cbc_hmac_t: TokenT = TokenT.CONF_EMAIL,
    existing_payload: RegisterPayloadT | None = None,
) -> GenTokensReturnT:
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

    if not reverse:
        assert REG_ID.fullmatch(
            res_register["data"]["access_token_decoded"]["user_id"]
        )

        assert REG_ID.fullmatch(
            res_register["data"]["refresh_token_db"]["user_id"]
        )
        assert REG_ID.fullmatch(
            res_register["data"]["refresh_token_decrypted"]["user_id"]
        )

        assert REG_ID.fullmatch(res_register["data"]["cbc_hmac_db"]["user_id"])
        assert REG_ID.fullmatch(
            res_register["data"]["cbc_hmac_decrypted"]["user_id"]
        )

        assert (
            res_register["data"]["cbc_hmac_decrypted"]["user_id"]
            == res_register["data"]["refresh_token_decrypted"]["user_id"]
            == res_register["data"]["access_token_decoded"]["user_id"]
        )

    return {
        "access_token": res_register["data"]["access_token"],
        "refresh_token": res_register["refresh_token"],
        "cbc_hmac_token": res_register["data"]["cbc_hmac_token"],
        "payload": payload,
    }
