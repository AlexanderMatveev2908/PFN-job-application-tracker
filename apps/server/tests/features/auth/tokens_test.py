from typing import Callable
import pytest
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient


@pytest.mark.asyncio
async def ok_t(api) -> None:
    await get_tokens_lib(api)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, act, mutate, expected_msg",
    [
        ("expired_jwt", "JWT", None, "jwt_expired"),
        ("expired_jwe", "JWE", None, "jwe_expired"),
        ("expired_cbc", "CBC_HMAC", None, "cbc_hmac_expired"),
        (
            "invalid_jwt",
            "JWT",
            lambda t: t[:-4] + "aaaa",
            "jwt_invalid",
        ),
        (
            "invalid_jwe",
            "JWE",
            lambda t: t[:-4] + "hack",
            "jwe_invalid",
        ),
        (
            "invalid_cbc",
            "CBC_HMAC",
            lambda t: t[:-4] + "aaaa",
            "cbc_hmac_invalid",
        ),
    ],
)
async def bad_cases_t(
    api: AsyncClient,
    case: str,
    act: str,
    mutate: Callable[[str], str],
    expected_msg: str,
) -> None:
    reverse = case.startswith("expired")
    res_tokens = await get_tokens_lib(api, reverse=reverse)

    url = f"/test/get-err?cbc_hmac_token_t={TokenT.CONF_EMAIL.value}"  # noqa: E501

    token_map = {
        "JWT": res_tokens["access_token"],
        "JWE": res_tokens["refresh_token"],
        "CBC_HMAC": res_tokens["cbc_hmac_token"],
    }

    token = token_map[act]
    if mutate:
        token = mutate(token)

    res = await wrap_httpx(
        api,
        url=url,
        data={"token": token, "act": act},
        expected_code=401,
    )

    assrt_msg(res, expected_msg)
