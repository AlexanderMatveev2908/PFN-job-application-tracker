import re
import pytest
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def test_tokens_ok(api) -> None:
    await get_tokens_lib(api)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, act, mutate, expected_msg",
    [
        ("expired_jwt", "JWT", None, "access_token_expired"),
        ("expired_jwe", "JWE", None, "refresh_token_expired"),
        ("expired_cbc", "CBC_HMAC", None, "cbc_hmac_expired"),
        (
            "invalid_jwt",
            "JWT",
            lambda t: t[:-4] + "aaaa",
            "access_token_invalid",
        ),
        (
            "invalid_jwe",
            "JWE",
            lambda t: t[:-4] + "hack",
            "refresh_token_invalid",
        ),
        (
            "invalid_cbc",
            "CBC_HMAC",
            lambda t: t[:-4] + "aaaa",
            "cbc_hmac_invalid",
        ),
    ],
)
async def test_tokens_invalid_cases(
    api, case, act, mutate, expected_msg
) -> None:
    reverse = case.startswith("expired")
    res_tokens = await get_tokens_lib(api, reverse=reverse)

    url = f"/test/get-err-{'expired' if reverse else 'invalid'}?cbc_hmac_token_t={TokenT.CONF_EMAIL.value}"  # noqa: E501

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

    assert re.compile(rf".*{expected_msg}$").fullmatch(
        res["data"]["msg"].lower()
    )
