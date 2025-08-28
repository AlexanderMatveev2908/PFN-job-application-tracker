from typing import cast
from httpx import AsyncClient
import pytest

from src.__dev_only.payloads import get_payload_register
from src.constants.reg import REG_SECRET_TOTP
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import (
    TokenArgT,
    get_tokens_lib,
)
from tests.conf.lib.get_us import get_verified_user_lib
from tests.conf.lib.idx import wrap_httpx

URL = "/user/2FA"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_us = await get_verified_user_lib(
        api,
    )

    res_2FA = await wrap_httpx(
        api,
        url="/user/2FA",
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
        ("jwt_expired", 401, "jwt_expired"),
        ("cbc_hmac_expired", 401, "cbc_hmac_expired"),
        ("jwt_invalid", 401, "jwt_invalid"),
        ("cbc_hmac_invalid", 401, "cbc_hmac_invalid"),
        ("cbc_hmac_wrong_type", 401, "cbc_hmac_wrong_type"),
        ("not_verified", 403, "user must be verified to set up 2fa"),
        ("already_setup", 409, "user already have 2fa set up"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:

    payload = get_payload_register()

    if case != "not_verified":
        res_us = await get_verified_user_lib(
            api,
            expired=cast(
                list[TokenArgT],
                (
                    [case.split("_expired")[0]]
                    if case.endswith("_expired")
                    else []
                ),
            ),
            token_t=TokenT[
                (
                    "CHANGE_EMAIL"
                    if "cbc_hmac_wrong_type" == case
                    else "MANAGE_ACC"
                )
            ],
        )
    else:
        res_us = await get_tokens_lib(
            api, cbc_hmac_t=TokenT.MANAGE_ACC, existing_payload=payload
        )

    jwt: str = res_us["access_token"]
    cbc_hmac: str = res_us["cbc_hmac_token"]

    if case == "already_setup":
        await wrap_httpx(
            api,
            url=URL,
            access_token=jwt,
            data={"cbc_hmac_token": cbc_hmac},
            expected_code=200,
            method="PATCH",
        )

    if case.endswith("_invalid"):
        if "jwt" in case:
            jwt = jwt[:-4] + "aaaa"
        elif "cbc_hmac" in case:
            cbc_hmac = cbc_hmac[:-4] + "aaaa"

    err_res = await wrap_httpx(
        api,
        url=URL,
        access_token=jwt,
        data={"cbc_hmac_token": cbc_hmac},
        expected_code=expected_code,
        method="PATCH",
    )

    assrt_msg(err_res, expected_msg)
