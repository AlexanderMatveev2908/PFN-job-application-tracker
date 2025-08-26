from httpx import AsyncClient
import pytest
from src.models.token import TokenT
from tests.conf.lib.data_structure import gen_totp, get_aad_cbc_hmac
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.login import get_logged_2fa


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_logged = await get_logged_2fa(api)

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
        url="/user/manage-account-2FA",
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
