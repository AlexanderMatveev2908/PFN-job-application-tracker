import pytest
from src.constants.reg import REG_JWE, REG_JWT
from src.lib.pwd_gen import gen_pwd
from src.models.token import TokenT
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx

URL = "/auth/recover-pwd"


@pytest.mark.asyncio
async def test_recover_pwd_ok(api) -> None:
    res_tokens = await get_tokens_lib(api, cbc_hmac_t=TokenT.RECOVER_PWD)

    new_pwd = gen_pwd(n=5)

    res_change = await wrap_httpx(
        api,
        url=URL,
        data={
            "cbc_hmac_token": res_tokens["cbc_hmac_token"],
            "password": new_pwd,
        },
        expected_code=200,
        method="PATCH",
    )

    assert REG_JWT.fullmatch(res_change["data"]["access_token"])
    assert REG_JWE.fullmatch(res_change["refresh_token"])
    assert "password updated" in res_change["data"]["msg"].lower()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("same_pwd", 400, "new password must be different from old one"),
        ("expired", 401, "cbc_hmac_expired"),
        ("wrong_type", 401, "cbc_hmac_wrong_type"),
    ],
)
async def test_recover_pwd_invalid_cases(
    api, case, expected_code, expected_msg
) -> None:
    new_pwd = gen_pwd(n=5)

    payload: dict | None = None

    if case == "same_pwd":
        res_tokens = await get_tokens_lib(api, cbc_hmac_t=TokenT.RECOVER_PWD)
        payload = {
            "cbc_hmac_token": res_tokens["cbc_hmac_token"],
            "password": res_tokens["payload"]["password"],
        }

    elif case == "expired":
        res_tokens = await get_tokens_lib(
            api, cbc_hmac_t=TokenT.RECOVER_PWD, reverse=True
        )
        payload = {
            "cbc_hmac_token": res_tokens["cbc_hmac_token"],
            "password": new_pwd,
        }

    elif case == "wrong_type":
        res_tokens = await get_tokens_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)
        payload = {
            "cbc_hmac_token": res_tokens["cbc_hmac_token"],
            "password": new_pwd,
        }

    res_change = await wrap_httpx(
        api,
        url=URL,
        data=payload,
        expected_code=expected_code,
        method="PATCH",
    )

    assert expected_msg in res_change["data"]["msg"].lower()
