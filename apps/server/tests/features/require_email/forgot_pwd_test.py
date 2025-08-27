import pytest
from src.lib.etc import grab
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

from tests.conf.lib.register import register_ok_lib

URL = "/require-email/recover-pwd"


@pytest.mark.asyncio
async def ok_t(api) -> None:
    res_register = await register_ok_lib(api)

    res_forgot_pwd = await wrap_httpx(
        api,
        url=URL,
        data={"email": grab(res_register, "email")},
        expected_code=201,
    )

    assrt_msg(res_forgot_pwd, "email sent")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("invalid_email", 422, None),
        ("not_found", 404, "user not found"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    payload: dict | None = None

    if case == "invalid_email":
        res_register = await register_ok_lib(api)
        payload = {"email": res_register["payload"]["email"] * 8}

    elif case == "not_found":
        payload = {"email": "example-non-existent@gmail.com"}

    res = await wrap_httpx(
        api, url=URL, data=payload, expected_code=expected_code
    )

    if expected_msg:
        assrt_msg(res, expected_msg)
