from typing import cast
from httpx import AsyncClient
import pytest
from src.lib.etc import grab
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg, get_aad_cbc_hmac
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.login import make_flow_log_2FA


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_logged = await make_flow_log_2FA(api)

    res_pwd = await wrap_httpx(
        api,
        url="/user/manage-account",
        access_token=res_logged["access_token"],
        expected_code=200,
        data={"password": res_logged["payload"]["password"]},
    )

    get_aad_cbc_hmac(
        token=res_pwd["data"]["cbc_hmac_token"], token_t=TokenT.MANAGE_ACC_2FA
    )

    res_backup = await wrap_httpx(
        api,
        url="/user/manage-account-2FA-backup-code",
        access_token=res_logged["access_token"],
        expected_code=200,
        data={
            "backup_code": res_logged["backup_codes"][0],
            "cbc_hmac_token": grab(res_pwd, "cbc_hmac_token"),
        },
    )

    get_aad_cbc_hmac(
        res_backup["data"]["cbc_hmac_token"], token_t=TokenT.MANAGE_ACC
    )

    assert res_backup["data"]["backup_codes_left"] == 7


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("wrong_pwd", 401, "invalid password"),
        ("wrong_code", 401, "backup_code_invalid"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    res_logged = await make_flow_log_2FA(api)

    pwd_user = res_logged["payload"]["password"]

    res_pwd = await wrap_httpx(
        api,
        url="/user/manage-account",
        access_token=res_logged["access_token"],
        expected_code=expected_code if case == "wrong_pwd" else 200,
        data={"password": pwd_user + ("wrong" if case == "wrong_pwd" else "")},
    )

    if case == "wrong_pwd":
        assrt_msg(res_pwd, expected_msg)
        return

    code = cast(list, grab(cast(dict, res_logged), "backup_codes"))[0]

    res_backup = await wrap_httpx(
        api,
        url="/user/manage-account-2FA-backup-code",
        access_token=res_logged["access_token"],
        expected_code=expected_code,
        data={
            "cbc_hmac_token": grab(cast(dict, res_pwd), "cbc_hmac_token"),
            "backup_code": "1234-1234" if case == "wrong_code" else code,
        },
    )

    assrt_msg(res_backup, expected_msg)
