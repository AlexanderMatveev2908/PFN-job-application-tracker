from httpx import AsyncClient
import pytest

from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.login import get_logged_2fa


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_logged = await get_logged_2fa(api)

    res_pwd = await wrap_httpx(
        api,
        url="/user/manage-account",
        data={"password": res_logged["payload"]["password"]},
        expected_code=200,
        access_token=res_logged["access_token"],
    )
