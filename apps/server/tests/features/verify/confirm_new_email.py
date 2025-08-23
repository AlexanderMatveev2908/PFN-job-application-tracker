import os
from httpx import AsyncClient
import pytest

from src.constants.reg import REG_JWE, REG_JWT
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx

URL = "/verify/new-email?cbc_hmac_token="


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
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

    res_tk_body = await get_tokens_lib(
        api, cbc_hmac_t=TokenT.CHANGE_EMAIL, existing_payload=res_tk["payload"]
    )

    res_verify = await wrap_httpx(
        api, url=f'{URL}{res_tk_body["cbc_hmac_token"]}', method="GET"
    )

    assert "email updated successfully" in res_verify["data"]["msg"]
    assert REG_JWT.fullmatch(res_verify["data"]["access_token"])
    assert REG_JWE.fullmatch(res_verify["refresh_token"])
