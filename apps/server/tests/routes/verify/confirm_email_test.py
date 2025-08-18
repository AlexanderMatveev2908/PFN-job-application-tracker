import re
from httpx import AsyncClient
import pytest

from src.constants.reg import REG_CBC_HMAC
from tests.conf.constants import PAYLOAD_REGISTER
from tests.conf.lib import wrap_httpx


@pytest.mark.asyncio
async def confirm_email_ok_t(api: AsyncClient) -> None:
    data_register, *_ = await wrap_httpx(
        api, data=PAYLOAD_REGISTER, url="/auth/register", expected_code=201
    )

    assert REG_CBC_HMAC.fullmatch(data_register["cbc_hmac_token"])

    data_conf, *_ = await wrap_httpx(
        api,
        method="GET",
        url=f'/verify/confirm-email?cbc_hmac_token={data_register["cbc_hmac_token"]}',  # noqa: E501
        expected_code=200,
    )

    assert data_conf["updated_user"]["is_verified"] is True


@pytest.mark.asyncio
async def confirm_email_expired_t(api: AsyncClient) -> None:
    data_register, *_ = await wrap_httpx(
        api,
        data=PAYLOAD_REGISTER,
        url="/test/get-tokens-expired",
        expected_code=200,
    )

    assert REG_CBC_HMAC.fullmatch(data_register["cbc_hmac_token"])

    data_conf, *_ = await wrap_httpx(
        api,
        method="GET",
        url=f'/verify/confirm-email?cbc_hmac_token={data_register["cbc_hmac_token"]}',  # noqa: E501
        expected_code=401,
    )

    assert "CBC_HMAC_EXPIRED" in data_conf["msg"]


@pytest.mark.asyncio
async def confirm_email_invalid_t(api: AsyncClient) -> None:
    data_register, *_ = await wrap_httpx(
        api,
        data=PAYLOAD_REGISTER,
        url="/test/get-tokens-expired",
        expected_code=200,
    )

    assert REG_CBC_HMAC.fullmatch(data_register["cbc_hmac_token"])

    data_conf, *_ = await wrap_httpx(
        api,
        method="GET",
        url=f'/verify/confirm-email?cbc_hmac_token={data_register["cbc_hmac_token"][:-4]+'afaf'}',  # noqa: E501
        expected_code=401,
    )

    assert re.compile(r".*CBC_HMAC_INVALID$").fullmatch(data_conf["msg"])
