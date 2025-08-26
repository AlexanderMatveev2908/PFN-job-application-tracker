import os
import pytest
from src.__dev_only.payloads import RegisterPayloadT
from src.constants.reg import REG_JWE, REG_JWT
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

URL = "/verify/new-email?cbc_hmac_token="


async def _local_wrapper(api) -> RegisterPayloadT:
    res_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)
    new_email = os.urandom(15).hex() + "@gmail.com"

    res_change = await wrap_httpx(
        api,
        url="/user/change-email",
        access_token=res_tk["access_token"],
        data={"email": new_email, "cbc_hmac_token": res_tk["cbc_hmac_token"]},
        expected_code=200,
        method="PATCH",
    )
    assert "email sent to new address" in res_change["data"]["msg"]

    return res_tk["payload"]


@pytest.mark.asyncio
async def test_confirm_new_email_ok(api) -> None:
    res_tk_body = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.CHANGE_EMAIL,
        existing_payload=await _local_wrapper(api),
    )

    res_verify = await wrap_httpx(
        api,
        url=f'{URL}{res_tk_body["cbc_hmac_token"]}',
        method="GET",
        expected_code=200,
    )

    assert "email updated successfully" in res_verify["data"]["msg"].lower()
    assert REG_JWT.fullmatch(res_verify["data"]["access_token"])
    assert REG_JWE.fullmatch(res_verify["refresh_token"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("wrong_type", 401, "cbc_hmac_wrong_type"),
        ("invalid", 401, "cbc_hmac_invalid"),
        ("expired", 401, "cbc_hmac_expired"),
    ],
)
async def test_confirm_new_email_invalid_cases(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    url = ""

    if case == "wrong_type":
        res_tk_body = await get_tokens_lib(
            api,
            cbc_hmac_t=TokenT.CONF_EMAIL,
            existing_payload=await _local_wrapper(api),
        )
        url = f'{URL}{res_tk_body["cbc_hmac_token"]}'

    elif case == "invalid":
        res_tk_body = await get_tokens_lib(
            api,
            cbc_hmac_t=TokenT.CHANGE_EMAIL,
            existing_payload=await _local_wrapper(api),
        )
        url = (
            f'{URL}{res_tk_body["cbc_hmac_token"][:-10]}{os.urandom(5).hex()}'
        )

    elif case == "expired":
        res_tk_body = await get_tokens_lib(
            api,
            cbc_hmac_t=TokenT.CHANGE_EMAIL,
            existing_payload=await _local_wrapper(api),
            reverse=True,
        )
        url = f'{URL}{res_tk_body["cbc_hmac_token"]}'

    res_verify = await wrap_httpx(
        api,
        url=url,
        method="GET",
        expected_code=expected_code,
    )

    assert expected_msg in res_verify["data"]["msg"].lower()
