import re
from httpx import AsyncClient
import pytest
from src.lib.data_structure import b_to_d, h_to_b
from src.models.token import TokenT
from tests.conf.lib import get_tokens_lib, register_ok_lib, wrap_httpx

URL = "/verify/confirm-email?cbc_hmac_token="


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_conf = await wrap_httpx(
        api,
        method="GET",
        url=f'{URL}{res_register["data_register"]["cbc_hmac_token"]}',  # noqa: E501
        expected_code=200,
    )

    assert res_conf["data"]["updated_user"]["is_verified"] is True


@pytest.mark.asyncio
async def err_already_verified_t(api: AsyncClient) -> None:
    res_register = await register_ok_lib(api)

    res_conf = await wrap_httpx(
        api,
        method="GET",
        url=f'{URL}{res_register["data_register"]["cbc_hmac_token"]}',  # noqa: E501
        expected_code=200,
    )

    assert res_conf["data"]["updated_user"]["is_verified"] is True

    res_tokens = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.CONF_EMAIL,
        existing_payload=res_register["payload"],
    )

    aad_d = b_to_d(h_to_b((res_tokens["cbc_hmac_token"]).split(".")[0]))
    assert TokenT(aad_d["token_t"]) == TokenT.CONF_EMAIL

    assert aad_d["user_id"] == res_conf["data"]["updated_user"]["id"]

    res_err = await wrap_httpx(
        api,
        method="GET",
        url=f'{URL}{res_tokens["cbc_hmac_token"]}',  # noqa: E501
        expected_code=409,
    )

    assert "user already verified" in res_err["data"]["msg"]


@pytest.mark.asyncio
async def err_expired_t(api: AsyncClient) -> None:
    res = await get_tokens_lib(api, reverse=True)

    res_conf = await wrap_httpx(
        api,
        method="GET",
        url=f"{URL}{res['cbc_hmac_token']}",  # noqa: E501
        expected_code=401,
    )

    assert "CBC_HMAC_EXPIRED" in res_conf["data"]["msg"]


@pytest.mark.asyncio
async def err_invalid_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(api, reverse=True)

    res_conf = await wrap_httpx(
        api,
        method="GET",
        url=f"{URL}{res_tokens['cbc_hmac_token'][:-4]+'afaf'}",  # noqa: E501
        expected_code=401,
    )

    assert re.compile(r".*CBC_HMAC_INVALID$").fullmatch(
        res_conf["data"]["msg"]
    )
