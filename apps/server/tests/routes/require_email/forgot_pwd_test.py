from httpx import AsyncClient
import pytest

from src.lib.data_structure import b_to_d, h_to_b
from src.models.token import TokenT
from tests.conf.lib import get_tokens_lib, register_ok_lib, wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res = await register_ok_lib(api)

    data_forgot_pwd, *_ = await wrap_httpx(
        api,
        data={"email": res["payload"]["email"]},
        url="/require-email/forgot-pwd",
        expected_code=201,
    )

    assert "email sent" in data_forgot_pwd["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    res = await get_tokens_lib(api, cbc_hmac_t=TokenT.RECOVER_PWD)

    assert (
        TokenT(b_to_d(h_to_b(res["cbc_hmac_token"].split(".")[0]))["token_t"])
        == TokenT.RECOVER_PWD
    )

    data, *_ = await wrap_httpx(
        api,
        url="/require-email/forgot-pwd",
        data={"email": res["payload"]["email"] * 8},
        expected_code=422,
    )
