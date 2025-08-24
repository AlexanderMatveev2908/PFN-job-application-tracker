import pytest
from src.constants.reg import REG_JWE, REG_JWT
from tests.conf.constants import get_payload_register
from tests.conf.lib.data_structure import extract_login_payload
from tests.conf.lib.etc import register_ok_lib
from tests.conf.lib.idx import wrap_httpx

URL = "/auth/login"


@pytest.mark.asyncio
async def test_login_ok(api) -> None:
    res_register = await register_ok_lib(api)

    res_login = await wrap_httpx(
        api,
        url=URL,
        data=extract_login_payload(res_register["payload"]),
        expected_code=200,
    )

    assert REG_JWE.fullmatch(res_login["refresh_token"])
    assert REG_JWT.fullmatch(res_login["data"]["access_token"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("not_found", 404, "user not found"),
        ("invalid_password", 401, "invalid credentials"),
    ],
)
async def test_login_invalid_cases(
    api, case, expected_code, expected_msg
) -> None:
    payload: dict | None = None

    if case == "not_found":
        payload = extract_login_payload(get_payload_register())

    elif case == "invalid_password":
        res_register = await register_ok_lib(api)
        payload = {
            **extract_login_payload(res_register["payload"]),
            "password": res_register["payload"]["password"] + "wrong",
        }

    res_login = await wrap_httpx(
        api, url=URL, data=payload, expected_code=expected_code
    )
    assert expected_msg in res_login["data"]["msg"].lower()
