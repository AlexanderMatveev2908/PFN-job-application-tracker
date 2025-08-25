from httpx import AsyncClient
import pytest

from src.constants.reg import REG_SECRET_TOTP
from src.models.token import TokenT
from tests.conf.lib.etc import (
    get_verified_user_lib,
)
from tests.conf.lib.idx import wrap_httpx

URL = "/user/2FA"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_us = await get_verified_user_lib(
        api,
    )

    res_2FA = await wrap_httpx(
        api,
        url=URL,
        method="PATCH",
        access_token=res_us["access_token"],
        data={"cbc_hmac_token": res_us["cbc_hmac_token"]},
        expected_code=200,
    )

    assert REG_SECRET_TOTP.fullmatch(res_2FA["data"]["totp_secret"])

    assert len(res_2FA["data"]["backup_codes"]) == 8


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("jwt_expired", 401, "access_token_expired"),
        ("cbc_hmac_expired", 401, "cbc_hmac_expired"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:

    res_us = await get_verified_user_lib(
        api,
        expired=(
            [case.split("_expired")[0]] if case.endswith("_expired") else []
        ),
        token_t=TokenT.MANAGE_ACC,
    )

    err_res = await wrap_httpx(
        api,
        url=URL,
        access_token=res_us["access_token"],
        data={"cbc_hmac_token": res_us["cbc_hmac_token"]},
        expected_code=expected_code,
        method="PATCH",
    )

    assert expected_msg in err_res["data"]["msg"].lower()
