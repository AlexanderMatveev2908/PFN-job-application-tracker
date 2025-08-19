from typing import Any, Literal
from httpx import AsyncClient, Response

from src.constants.reg import REG_CBC_HMAC, REG_JWE, REG_JWT
from src.lib.logger import clg
from tests.conf.constants import RegisterPayloadT, get_payload_register


def parse_res(res: Response) -> dict:
    data = res.json()

    full = str(res.request.url)
    part = (
        full[full.index("/api/v1") + len("/api/v1") :]  # noqa: E203
    ).split("?", 1)[0]

    if res.status_code not in [200, 201]:
        clg(
            data,
            ttl=f"💾 {part} — 🚦 {res.status_code}",
        )

    return data


async def wrap_httpx(
    api: AsyncClient,
    *,
    url: str,
    method: Literal["POST", "GET"] = "POST",
    data: Any | None = None,
    expected_code: int = 200,
) -> tuple[dict[Literal["msg"] | str, Any], str]:

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

    except Exception as err:
        clg(str(err), ttl="err assertion")
        raise err

    return (parsed, refresh)


def extract_login_payload(
    payload_register: RegisterPayloadT,
) -> dict[Literal["email", "password"], str]:
    return {
        "email": payload_register["email"],
        "password": payload_register["password"],
    }


async def register_ok_lib(api) -> tuple[RegisterPayloadT, dict]:
    payload = get_payload_register()

    data_register, refresh_token = await wrap_httpx(
        api,
        url="/auth/register",
        data=payload,
        expected_code=201,
    )

    assert REG_JWT.fullmatch(data_register["access_token"])
    assert REG_JWE.fullmatch(refresh_token)
    assert REG_CBC_HMAC.fullmatch(data_register["cbc_hmac_token"])
    assert "new_user" in data_register

    return (payload, data_register)
