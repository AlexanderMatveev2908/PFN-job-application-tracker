import re
import pytest
from src.lib.data_structure import b_to_d, h_to_b
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

URL = "/verify/confirm-email?cbc_hmac_token="


@pytest.mark.asyncio
async def test_confirm_email_ok(api) -> None:
    res_register = await get_tokens_lib(api)

    res_conf = await wrap_httpx(
        api,
        method="GET",
        url=f'{URL}{res_register["cbc_hmac_token"]}',
        expected_code=200,
    )

    assert res_conf["data"]["updated_user"]["is_verified"] is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("already_verified", 409, "user already verified"),
        ("expired", 401, "CBC_HMAC_EXPIRED"),
        ("invalid", 401, re.compile(r".*CBC_HMAC_INVALID$")),
    ],
)
async def test_confirm_email_invalid_cases(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    url = ""

    if case == "already_verified":
        res_register = await get_tokens_lib(api)

        res_conf = await wrap_httpx(
            api,
            method="GET",
            url=f'{URL}{res_register["cbc_hmac_token"]}',
            expected_code=200,
        )
        assert res_conf["data"]["updated_user"]["is_verified"] is True

        res_tokens = await get_tokens_lib(
            api, existing_payload=res_register["payload"]
        )
        aad_d = b_to_d(h_to_b((res_tokens["cbc_hmac_token"]).split(".")[0]))
        assert TokenT(aad_d["token_t"]) == TokenT.CONF_EMAIL
        assert aad_d["user_id"] == res_conf["data"]["updated_user"]["id"]

        url = f'{URL}{res_tokens["cbc_hmac_token"]}'

    elif case == "expired":
        res_tokens = await get_tokens_lib(api, reverse=True)
        url = f"{URL}{res_tokens['cbc_hmac_token']}"

    elif case == "invalid":
        res_tokens = await get_tokens_lib(api, reverse=True)
        url = f"{URL}{res_tokens['cbc_hmac_token'][:-4]}afaf"

    res_conf = await wrap_httpx(
        api, method="GET", url=url, expected_code=expected_code
    )

    if isinstance(expected_msg, re.Pattern):
        assert expected_msg.fullmatch(res_conf["data"]["msg"])
    else:
        assert expected_msg in res_conf["data"]["msg"]
