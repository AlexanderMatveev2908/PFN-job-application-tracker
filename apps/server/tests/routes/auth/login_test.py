from httpx import AsyncClient
import pytest

from src.constants.reg import REG_JWE, REG_JWT
from tests.conf.constants import get_payload_register
from tests.conf.lib import wrap_httpx


@pytest.mark.asyncio
async def login_ok_t(api: AsyncClient) -> None:
    payload = get_payload_register()

    data_register, *_ = await wrap_httpx(
        api,
        url="/auth/register",
        data=payload,
        expected_code=201,
    )

    assert REG_JWT.fullmatch(data_register["access_token"])

    data_login, refresh_token = await wrap_httpx(
        api,
        url="/auth/login",
        data={"email": payload["email"], "password": payload["password"]},
        expected_code=200,
    )

    assert REG_JWE.fullmatch(refresh_token)
    assert REG_JWT.fullmatch(data_login["access_token"])
