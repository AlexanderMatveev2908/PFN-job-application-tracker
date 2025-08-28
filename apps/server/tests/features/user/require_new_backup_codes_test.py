from httpx import AsyncClient
import pytest
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg, gen_totp
from tests.conf.lib.get_us import get_us_2FA_lib
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.login import make_flow_log_2FA


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_logged = await make_flow_log_2FA(api, cbc_hmac_t=TokenT.MANAGE_ACC)

    res_err = await wrap_httpx(
        api,
        url="/user/new-backup-codes",
        access_token=res_logged["access_token"],
        expected_code=409,
        data={"cbc_hmac_token": res_logged["cbc_hmac_token"]},
    )

    assrt_msg(res_err, "user already has backup codes")

    res_no_codes = await get_us_2FA_lib(api, empty_codes=True)

    res_manage_0 = await wrap_httpx(
        api,
        url="/user/manage-account",
        access_token=res_no_codes["access_token"],
        expected_code=200,
        data={"password": res_no_codes["payload"]["password"]},
    )

    res_manage_1 = await wrap_httpx(
        api,
        url="/user/manage-account-2FA",
        access_token=res_no_codes["access_token"],
        expected_code=200,
        data={
            "cbc_hmac_token": res_manage_0["data"]["cbc_hmac_token"],
            "totp_code": gen_totp(res_no_codes["totp_secret"]),
        },
    )

    res_new_codes = await wrap_httpx(
        api,
        url="/user/new-backup-codes",
        access_token=res_no_codes["access_token"],
        expected_code=200,
        data={"cbc_hmac_token": res_manage_1["data"]["cbc_hmac_token"]},
    )

    codes = res_new_codes["data"]["backup_codes"]
    assert isinstance(codes, list)
    assert len(codes) == 8


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("cbc_hmac_expired", 401, "cbc_hmac_expired"),
        ("cbc_hmac_invalid", 401, "cbc_hmac_invalid"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    res_logged = await get_us_2FA_lib(
        api,
        expired=case.split("_expired"),
        cbc_hmac_t=TokenT.MANAGE_ACC,
        empty_codes=True,
    )

    token_manage = res_logged["cbc_hmac_token"]

    if case == "cbc_hmac_invalid":
        token_manage = token_manage[:-4] + "aaf2"

    res_require = await wrap_httpx(
        api,
        url="/user/new-backup-codes",
        access_token=res_logged["access_token"],
        expected_code=expected_code,
        data={"cbc_hmac_token": token_manage},
    )

    assrt_msg(res_require, expected_msg)
