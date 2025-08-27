import faker
from httpx import AsyncClient
import pytest

from src.lib.etc import grab
from src.models.token import TokenT
from tests.conf.lib.data_structure import (
    assrt_msg,
    assrt_sessions_tokens,
    gen_totp,
    get_aad_cbc_hmac,
)
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.get_us import get_us_2FA_lib
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_logged = await get_us_2FA_lib(api, cbc_hmac_t=TokenT.MANAGE_ACC)

    new_email = faker.Faker().email()

    res_change = await wrap_httpx(
        api,
        url="/user/change-email",
        access_token=res_logged["access_token"],
        expected_code=200,
        data={
            "email": new_email,
            "cbc_hmac_token": res_logged["cbc_hmac_token"],
        },
        method="PATCH",
    )

    assrt_msg(res_change, "email sent")

    tokens_res = await get_tokens_lib(
        api,
        existing_payload=res_logged["payload"],
        cbc_hmac_t=TokenT.CHANGE_EMAIL,
    )

    res_verify_0 = await wrap_httpx(
        api,
        url=f"/verify/new-email?cbc_hmac_token={tokens_res['cbc_hmac_token']}",
        expected_code=200,
        method="GET",
    )

    token_verify = grab(res_verify_0, "cbc_hmac_token")
    get_aad_cbc_hmac(
        token=token_verify,
        token_t=TokenT.CHANGE_EMAIL_2FA,
    )

    res_verify_1 = await wrap_httpx(
        api,
        url="/verify/new-email-2FA-totp",
        method="PATCH",
        expected_code=200,
        data={
            "cbc_hmac_token": token_verify,
            "totp_code": gen_totp(
                totp_secret=grab(
                    res_logged,
                    "totp_secret",
                ),
            ),
        },
    )

    assrt_sessions_tokens(res_verify_1)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("wrong_code", 401, "totp_code_invalid"),
        ("cbc_hmac_expired", 401, "cbc_hmac_expired"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    res_2fa = await get_us_2FA_lib(api)

    new_email = faker.Faker().email()

    res_change = await wrap_httpx(
        api,
        url="/user/change-email",
        method="PATCH",
        expected_code=200,
        data={
            "email": new_email,
            "cbc_hmac_token": res_2fa["cbc_hmac_token"],
        },
        access_token=res_2fa["access_token"],
    )

    assrt_msg(res_change, "email sent")

    res_verify = await wrap_httpx(
        api,
        url=f"/verify/new-email?cbc_hmac_token={(await get_tokens_lib(api, existing_payload=res_2fa["payload"], cbc_hmac_t=TokenT.CHANGE_EMAIL))['cbc_hmac_token']}",  # noqa: E501
        method="GET",
    )

    token_2fa = (
        (
            await get_tokens_lib(
                api,
                existing_payload=res_2fa["payload"],
                cbc_hmac_t=TokenT.CHANGE_EMAIL_2FA,
                expired=["cbc_hmac"],
            )
        )["cbc_hmac_token"]
        if case == "cbc_hmac_expired"
        else grab(res_verify, "cbc_hmac_token")
    )

    get_aad_cbc_hmac(token_2fa, TokenT.CHANGE_EMAIL_2FA)

    res_totp = await wrap_httpx(
        api,
        url="/verify/new-email-2FA-totp",
        method="PATCH",
        data={
            "cbc_hmac_token": token_2fa,
            "totp_code": (
                "123456"
                if case == "wrong_code"
                else gen_totp(res_2fa["totp_secret"])
            ),
        },
        expected_code=expected_code,
    )

    assrt_msg(res_totp, expected_msg)
