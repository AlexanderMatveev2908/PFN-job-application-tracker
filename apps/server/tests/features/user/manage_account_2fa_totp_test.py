from httpx import AsyncClient
import pytest
from src.models.token import TokenT
from tests.conf.lib.data_structure import gen_totp, get_aad_cbc_hmac
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.login import make_flow_log_2FA


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_logged = await make_flow_log_2FA(api)

    res_pwd = await wrap_httpx(
        api,
        url="/user/manage-account",
        data={"password": res_logged["payload"]["password"]},
        expected_code=200,
        access_token=res_logged["access_token"],
    )

    get_aad_cbc_hmac(
        res_pwd["data"]["cbc_hmac_token"], token_t=TokenT.MANAGE_ACC_2FA
    )

    res_err = await wrap_httpx(
        api,
        url=f"/user/delete-account?cbc_hmac_token={res_pwd['data']['cbc_hmac_token']}",  # noqa: E501
        access_token=res_logged["access_token"],
        expected_code=401,
        method="DELETE",
    )

    assert "cbc_hmac_wrong_type" in res_err["data"]["msg"]

    res_totp = await wrap_httpx(
        api,
        url="/user/manage-account-2FA-totp",
        access_token=res_logged["access_token"],
        data={
            "totp_code": gen_totp(res_logged["totp_secret"]),
            "cbc_hmac_token": res_pwd["data"]["cbc_hmac_token"],
        },
        expected_code=200,
    )

    get_aad_cbc_hmac(
        token=res_totp["data"]["cbc_hmac_token"], token_t=TokenT.MANAGE_ACC
    )

    res_delete = await wrap_httpx(
        api,
        url=f"/user/delete-account?cbc_hmac_token={res_totp['data']['cbc_hmac_token']}",  # noqa: E501
        access_token=res_logged["access_token"],
        method="DELETE",
        expected_code=200,
    )

    assert "user account deleted" in res_delete["data"]["msg"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("cbc_hmac_invalid", 401, "cbc_hmac_invalid"),
        ("cbc_hmac_expired", 401, "cbc_hmac_expired"),
        ("totp_invalid", 401, "totp_code_invalid"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    res_logged = await make_flow_log_2FA(api)

    res_tokens = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.MANAGE_ACC_2FA,
        existing_payload=res_logged["payload"],
        expired=case.split("_expired"),
    )

    totp_code = (
        "123456"
        if case == "totp_invalid"
        else gen_totp(res_logged["totp_secret"])
    )

    token_2fa = res_tokens["cbc_hmac_token"]
    if case == "cbc_hmac_invalid":
        token_2fa = token_2fa[:-4] + "a2fa"

    res_totp = await wrap_httpx(
        api,
        url="/user/manage-account-2FA-totp",
        access_token=res_logged["access_token"],
        data={
            "totp_code": totp_code,
            "cbc_hmac_token": token_2fa,
        },
        expected_code=expected_code,
    )

    assert expected_msg in res_totp["data"]["msg"]
