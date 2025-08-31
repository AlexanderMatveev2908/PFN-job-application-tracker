from httpx import AsyncClient
import pytest

from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(api)

    assert "refresh_token" in api.cookies

    res_logout = await wrap_httpx(
        api,
        url="/auth/logout",
        access_token=res_tokens["access_token"],
        expected_code=200,
    )

    assert "refresh_token" not in api.cookies

    assrt_msg(res_logout, "logout successful")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("jwt_expired", 401, "jwt_expired"),
        ("ignore_err", 200, "logout almost successful"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    access_token = ""

    if case != "ignore_err":
        res_tokens = await get_tokens_lib(api, expired=case.split("_expired"))
        access_token = res_tokens["access_token"]

    res_logout = await wrap_httpx(
        api,
        url="/auth/logout",
        access_token=access_token,
        expected_code=expected_code,
    )

    assrt_msg(res_logout, expected_msg)
