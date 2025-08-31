from httpx import AsyncClient
import pytest

from src.constants.reg import REG_ID
from src.decorators.err import ErrAPI
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(api)

    res_profile = await wrap_httpx(
        api,
        url="/user/profile",
        access_token=res_tokens["access_token"],
        method="GET",
        expected_code=200,
    )

    us = res_profile["data"]["user"]

    assert REG_ID.fullmatch(us["id"])

    for k in us:
        if k in ["password", "totp_secret"]:
            raise ErrAPI(msg="danger secrets user", status=500)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [("jwt_expired", 401, "jwt_expired"), ("ignored", 204, "")],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    access_token = ""

    if case != "ignored":
        access_token = (
            await get_tokens_lib(api, expired=case.split("_expired"))
        )["access_token"]

    res_profile = await wrap_httpx(
        api,
        url="/user/profile",
        access_token=access_token,
        expected_code=expected_code,
        method="GET",
    )

    if expected_msg:
        assrt_msg(res_profile, expected_msg)

    assert res_profile["data"].get("user") is None
