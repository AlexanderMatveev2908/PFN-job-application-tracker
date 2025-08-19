import re
from httpx import AsyncClient
import pytest
from tests.conf.lib import get_tokens_lib, register_ok_lib, wrap_httpx


@pytest.mark.asyncio
async def confirm_email_ok_t(api: AsyncClient) -> None:
    _, data_register = await register_ok_lib(api)

    data_conf, *_ = await wrap_httpx(
        api,
        method="GET",
        url=f'/verify/confirm-email?cbc_hmac_token={data_register["cbc_hmac_token"]}',  # noqa: E501
        expected_code=200,
    )

    assert data_conf["updated_user"]["is_verified"] is True


@pytest.mark.asyncio
async def confirm_email_expired_t(api: AsyncClient) -> None:
    *_, cbc_hmac_tk = await get_tokens_lib(api)

    data_conf, *_ = await wrap_httpx(
        api,
        method="GET",
        url=f"/verify/confirm-email?cbc_hmac_token={cbc_hmac_tk}",  # noqa: E501
        expected_code=401,
    )

    assert "CBC_HMAC_EXPIRED" in data_conf["msg"]


@pytest.mark.asyncio
async def confirm_email_invalid_t(api: AsyncClient) -> None:
    *_, cbc_hmac_tk = await get_tokens_lib(api)

    data_conf, *_ = await wrap_httpx(
        api,
        method="GET",
        url=f"/verify/confirm-email?cbc_hmac_token={cbc_hmac_tk[:-4]+'afaf'}",  # noqa: E501
        expected_code=401,
    )

    assert re.compile(r".*CBC_HMAC_INVALID$").fullmatch(data_conf["msg"])
