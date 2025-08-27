import pytest
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

from tests.conf.lib.register import register_ok_lib

URL = "/require-email/confirm-email"


@pytest.mark.asyncio
async def ok_t(api) -> None:
    res_register = await register_ok_lib(api)

    res_require = await wrap_httpx(
        api,
        url=URL,
        data={"email": res_register["payload"]["email"]},
        expected_code=201,
    )

    assert "email sent" in res_require["data"]["msg"].lower()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("invalid_email", 422, None),
        ("not_found", 404, "user not found"),
        ("already_confirmed", 409, "user already verified"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    payload: dict | None = None

    if case == "invalid_email":
        payload = {"email": "<><>/!"}

    elif case == "not_found":
        payload = {"email": "non-existent@gmail.com"}

    elif case == "already_confirmed":
        res_tokens = await get_tokens_lib(api)
        res_verify = await wrap_httpx(
            api,
            url=f'/verify/confirm-email?cbc_hmac_token={res_tokens["cbc_hmac_token"]}',  # noqa: E501
            expected_code=200,
            method="GET",
        )
        assert "email verified" in res_verify["data"]["msg"].lower()
        payload = {"email": res_tokens["payload"]["email"]}

    res = await wrap_httpx(
        api,
        url=URL,
        data=payload,
        expected_code=expected_code,
    )

    if expected_msg:
        assrt_msg(res, expected_msg)
