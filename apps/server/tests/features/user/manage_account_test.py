from httpx import AsyncClient
import pytest

from src.constants.reg import REG_CBC_HMAC
from tests.conf.lib.etc import register_ok_lib
from tests.conf.lib.idx import wrap_httpx

URL = "/user/manage-account"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_manage = await wrap_httpx(
        api,
        url=URL,
        data={"password": res_register["payload"]["password"]},
        access_token=res_register["data_register"]["access_token"],
        expected_code=200,
    )

    assert REG_CBC_HMAC.fullmatch(res_manage["data"]["cbc_hmac_token"])
