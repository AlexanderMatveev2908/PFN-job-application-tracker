from httpx import AsyncClient
import pytest

from src.constants.reg import REG_JWT
from tests.conf.constants import get_payload_register
from tests.conf.lib import wrap_httpx


@pytest.mark.asyncio
async def require_email_ok_t(api: AsyncClient) -> None:
    payload = get_payload_register()

    data_register, *_ = await wrap_httpx(
        api, data=payload, url="/auth/register", expected_code=201
    )

    assert REG_JWT.fullmatch(data_register["access_token"])

    data_forgot_pwd, *_ = await wrap_httpx(
        api,
        data={"email": payload["email"]},
        url="/require-email/forgot-pwd",
        expected_code=201,
    )

    assert "email sent" in data_forgot_pwd["msg"]
