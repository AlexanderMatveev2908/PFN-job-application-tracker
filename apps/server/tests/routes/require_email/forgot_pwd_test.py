from httpx import AsyncClient
import pytest

from src.lib.data_structure import b_to_d, h_to_b
from src.models.token import TokenT
from tests.conf.lib import get_tokens_lib, register_ok_lib, wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    payload, *_ = await register_ok_lib(api)

    data_forgot_pwd, *_ = await wrap_httpx(
        api,
        data={"email": payload["email"]},
        url="/require-email/forgot-pwd",
        expected_code=201,
    )

    assert "email sent" in data_forgot_pwd["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    *_, cbc_hmac_tk = await get_tokens_lib(api, cbc_hmac_t=TokenT.RECOVER_PWD)

    assert (
        TokenT(b_to_d(h_to_b(cbc_hmac_tk.split(".")[0]))["token_t"])
        == TokenT.RECOVER_PWD
    )
