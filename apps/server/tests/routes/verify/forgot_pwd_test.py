from httpx import AsyncClient
import pytest

from src.models.token import TokenT
from tests.conf.lib import get_tokens_lib, wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:

    res_tokens = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.RECOVER_PWD,
    )

    res_check_tk = await wrap_httpx(
        api,
        url=f'/verify/forgot-pwd?cbc_hmac_token={res_tokens["cbc_hmac_token"]}',  # noqa: E501
        expected_code=200,
        method="GET",
    )
