import re
from httpx import AsyncClient
import pytest
from src.lib.data_structure import b_to_d, h_to_b
from src.models.token import TokenT
from tests.conf.lib import get_tokens_lib, register_ok_lib, wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res = await register_ok_lib(api)

    data_conf, *_ = await wrap_httpx(
        api,
        method="GET",
        url=f'/verify/confirm-email?cbc_hmac_token={res["data_register"]["cbc_hmac_token"]}',  # noqa: E501
        expected_code=200,
    )

    assert data_conf["updated_user"]["is_verified"] is True


@pytest.mark.asyncio
async def err_already_verified_t(api: AsyncClient) -> None:
    res = await register_ok_lib(api)

    data_conf, *_ = await wrap_httpx(
        api,
        method="GET",
        url=f'/verify/confirm-email?cbc_hmac_token={res["data_register"]["cbc_hmac_token"]}',  # noqa: E501
        expected_code=200,
    )

    assert data_conf["updated_user"]["is_verified"] is True

    res_tokens = await get_tokens_lib(
        api,
        health=True,
        cbc_hmac_t=TokenT.CONF_EMAIL,
        existing_payload=res["payload"],
    )

    aad_d = b_to_d(h_to_b((res_tokens["cbc_hmac_token"]).split(".")[0]))
    assert TokenT(aad_d["token_t"]) == TokenT.CONF_EMAIL

    assert aad_d["user_id"] == data_conf["updated_user"]["id"]

    res_err, *_ = await wrap_httpx(
        api,
        method="GET",
        url=f'/verify/confirm-email?cbc_hmac_token={res_tokens["cbc_hmac_token"]}',  # noqa: E501
        expected_code=409,
    )

    assert "user already verified" in res_err["msg"]


@pytest.mark.asyncio
async def err_expired_t(api: AsyncClient) -> None:
    res = await get_tokens_lib(api)

    data_conf, *_ = await wrap_httpx(
        api,
        method="GET",
        url=f"/verify/confirm-email?cbc_hmac_token={res['cbc_hmac_token']}",  # noqa: E501
        expected_code=401,
    )

    assert "CBC_HMAC_EXPIRED" in data_conf["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    res = await get_tokens_lib(api)

    data_conf, *_ = await wrap_httpx(
        api,
        method="GET",
        url=f"/verify/confirm-email?cbc_hmac_token={res['cbc_hmac_token'][:-4]+'afaf'}",  # noqa: E501
        expected_code=401,
    )

    assert re.compile(r".*CBC_HMAC_INVALID$").fullmatch(data_conf["msg"])
