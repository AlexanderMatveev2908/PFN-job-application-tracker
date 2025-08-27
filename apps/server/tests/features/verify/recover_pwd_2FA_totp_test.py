from httpx import AsyncClient
import pytest

from src.lib.etc import grab
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.get_us import get_us_2FA_lib
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_logged = await get_us_2FA_lib(api)

    res_require = await wrap_httpx(
        api,
        url="/require-email/recover-pwd",
        data={
            "email": grab(res_logged, "email"),
        },
        expected_code=201,
    )

    assrt_msg(res_require, "email sent")
