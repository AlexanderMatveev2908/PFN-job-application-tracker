import os
from httpx import AsyncClient
import pytest

from src.lib.etc import grab
from src.models.token import TokenT
from tests.conf.lib.data_structure import (
    assrt_msg,
    assrt_sessions_tokens,
    get_aad_cbc_hmac,
)
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.get_us import get_us_2FA_lib
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_2fa = await get_us_2FA_lib(
        api,
    )

    await wrap_httpx(
        api,
        url="/user/change-email",
        data={
            "email": grab(res_2fa, "first_name")[:-20]
            + os.urandom(10).hex()
            + "@gmail.com",
            "cbc_hmac_token": res_2fa["cbc_hmac_token"],
        },
        access_token=res_2fa["access_token"],
        method="PATCH",
    )

    token_verify = (
        await get_tokens_lib(
            api,
            existing_payload=res_2fa["payload"],
            cbc_hmac_t=TokenT.CHANGE_EMAIL,
        )
    )["cbc_hmac_token"]

    res_verify = await wrap_httpx(
        api,
        url=f"/verify/new-email?cbc_hmac_token={token_verify}",
        method="GET",
        expected_code=200,
    )

    token_2fa = grab(res_verify, "cbc_hmac_token")

    get_aad_cbc_hmac(token_2fa, TokenT.CHANGE_EMAIL_2FA)

    res_verify_code = await wrap_httpx(
        api,
        url="/verify/new-email-2FA",
        data={
            "cbc_hmac_token": token_2fa,
            "backup_code": res_2fa["backup_codes"][0],
        },
        method="PATCH",
        expected_code=200,
    )

    assrt_sessions_tokens(res_verify_code)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("wrong_code", 401, "backup_code_invalid"),
        ("cbc_hmac_expired", 401, "cbc_hmac_expired"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    res_2fa = await get_us_2FA_lib(
        api,
    )

    await wrap_httpx(
        api,
        url="/user/change-email",
        data={
            "email": grab(res_2fa, "first_name")[:-20]
            + os.urandom(10).hex()
            + "@gmail.com",
            "cbc_hmac_token": res_2fa["cbc_hmac_token"],
        },
        access_token=res_2fa["access_token"],
        method="PATCH",
    )

    token_verify = (
        await get_tokens_lib(
            api,
            existing_payload=res_2fa["payload"],
            cbc_hmac_t=TokenT.CHANGE_EMAIL,
        )
    )["cbc_hmac_token"]

    res_verify = await wrap_httpx(
        api,
        url=f"/verify/new-email?cbc_hmac_token={token_verify}",
        method="GET",
        expected_code=200,
    )

    token_2fa = (
        (
            await get_tokens_lib(
                api,
                existing_payload=res_2fa["payload"],
                cbc_hmac_t=TokenT.CHANGE_EMAIL_2FA,
                expired=list(filter(None, case.split("_expired"))),
            )
        )["cbc_hmac_token"]
        if case == "cbc_hmac_expired"
        else grab(res_verify, "cbc_hmac_token")
    )

    get_aad_cbc_hmac(token_2fa, TokenT.CHANGE_EMAIL_2FA)

    res_verify_code = await wrap_httpx(
        api,
        url="/verify/new-email-2FA",
        data={
            "cbc_hmac_token": token_2fa,
            "backup_code": (
                "1234-5678"
                if case == "wrong_code"
                else res_2fa["backup_codes"][0]
            ),
        },
        method="PATCH",
        expected_code=expected_code,
    )

    assrt_msg(res_verify_code, expected_msg)
