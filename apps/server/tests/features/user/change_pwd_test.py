import os
from httpx import AsyncClient
import pytest

from src.constants.reg import REG_CBC_HMAC
from tests.conf.lib.etc import register_ok_lib
from tests.conf.lib.idx import wrap_httpx

URL_MNG = "/user/manage-account"
URL_CHG = "/user/change-pwd"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_manage = await wrap_httpx(
        api,
        url=URL_MNG,
        access_token=res_register["access_token"],
        data={"password": res_register["payload"]["password"]},
        expected_code=200,
    )

    assert REG_CBC_HMAC.fullmatch(res_manage["data"]["cbc_hmac_token"])

    res_change = await wrap_httpx(
        api,
        url=URL_CHG,
        expected_code=200,
        data={
            "password": res_register["payload"]["password"]
            + (os.urandom(5).hex()),
            "cbc_hmac_token": res_manage["data"]["cbc_hmac_token"],
        },
        access_token=res_register["access_token"],
        method="PATCH",
    )

    assert "password updated" in res_change["data"]["msg"]
