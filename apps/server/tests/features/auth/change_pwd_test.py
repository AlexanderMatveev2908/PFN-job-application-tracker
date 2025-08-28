import pytest
from src.lib.pwd_gen import gen_pwd
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_sessions_tokens
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

URL = "/auth/recover-pwd"


@pytest.mark.asyncio
async def ok_t(api) -> None:
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

    assrt_sessions_tokens(res_change)
    assert "password updated" in res_change["data"]["msg"].lower()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("same_pwd", 400, "new password must be different from old one"),
        ("cbc_hmac_expired", 401, "cbc_hmac_expired"),
        ("wrong_type", 401, "cbc_hmac_wrong_type"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:

    res_tokens = await get_tokens_lib(
        api,
        cbc_hmac_t=(
            TokenT.MANAGE_ACC if case == "wrong_type" else TokenT.RECOVER_PWD
        ),
        expired=case.split("_expired"),
    )

    payload = {
        "cbc_hmac_token": res_tokens["cbc_hmac_token"],
        "password": (
            res_tokens["payload"]["password"]
            if case == "same_pwd"
            else gen_pwd(n=5)
        ),
    }

    res_change = await wrap_httpx(
        api,
        url=URL,
        data=payload,
        expected_code=expected_code,
        method="PATCH",
    )

    assert expected_msg in res_change["data"]["msg"].lower()
