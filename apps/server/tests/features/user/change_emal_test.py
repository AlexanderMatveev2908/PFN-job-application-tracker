import os
from httpx import AsyncClient
import pytest

from src.constants.reg import REG_CBC_HMAC
from tests.conf.lib.etc import register_ok_lib
from tests.conf.lib.idx import wrap_httpx

URL = "/user/change-email"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_manage = await wrap_httpx(
        api,
        url="/user/manage-account",
        data={"password": res_register["payload"]["password"]},
        access_token=res_register["access_token"],
        expected_code=200,
    )

    assert REG_CBC_HMAC.fullmatch(res_manage["data"]["cbc_hmac_token"])

    new_email = os.urandom(20).hex() + "@gmail.com"

    res_mail = await wrap_httpx(
        api,
        url=URL,
        data={
            "email": new_email,
            "cbc_hmac_token": res_manage["data"]["cbc_hmac_token"],
        },
        access_token=res_register["access_token"],
        expected_code=200,
        method="PATCH",
    )

    assert "email sent to new address" in res_mail["data"]["msg"]
