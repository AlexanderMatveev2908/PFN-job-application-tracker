from httpx import AsyncClient
import pytest

from tests.conf.lib.etc import register_ok_lib
from tests.conf.lib.idx import wrap_httpx

URL = "/user/delete-account?cbc_hmac_token="


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_manage = await wrap_httpx(
        api,
        url="/user/manage-account",
        access_token=res_register["access_token"],
        expected_code=200,
        data={"password": res_register["payload"]["password"]},
    )

    res_delete = await wrap_httpx(
        api,
        url=URL + res_manage["data"]["cbc_hmac_token"],
        method="DELETE",
        access_token=res_register["access_token"],
        expected_code=200,
    )

    assert "account deleted" in res_delete["data"]["msg"]
