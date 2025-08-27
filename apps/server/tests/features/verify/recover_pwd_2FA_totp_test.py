from httpx import AsyncClient
import pytest

from src.constants.reg import REG_JWE, REG_JWT
from src.lib.etc import grab
from src.lib.pwd_gen import gen_pwd
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg, gen_totp, get_aad_cbc_hmac
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.get_us import get_us_2FA_lib
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_logged = await get_us_2FA_lib(api)

    res_require = await wrap_httpx(
        api,
        url="/require-email/recover-pwd",
        data={
            "email": grab(res_logged, "email"),
        },
        expected_code=201,
    )

    assrt_msg(res_require, "email sent")

    tokens_res = await get_tokens_lib(
        api,
        existing_payload=res_logged["payload"],
        cbc_hmac_t=TokenT.RECOVER_PWD,
    )

    get_aad_cbc_hmac(tokens_res["cbc_hmac_token"], TokenT.RECOVER_PWD)

    res_verify = await wrap_httpx(
        api,
        url=f"/verify/recover-pwd?cbc_hmac_token={grab(tokens_res, 'cbc_hmac_token')}",  # noqa: E501
        expected_code=200,
        method="GET",
    )

    res_err = await wrap_httpx(
        api,
        url="/auth/recover-pwd",
        method="PATCH",
        data={
            "password": gen_pwd(5),
            "cbc_hmac_token": tokens_res["cbc_hmac_token"],
        },
        expected_code=401,
    )

    assrt_msg(res_err, "cbc_hmac_not_found")

    get_aad_cbc_hmac(
        grab(res_verify, "cbc_hmac_token"), TokenT.RECOVER_PWD_2FA
    )

    res_totp = await wrap_httpx(
        api,
        url="/verify/recover-pwd-2FA-totp",
        data={
            "cbc_hmac_token": grab(res_verify, "cbc_hmac_token"),
            "totp_code": gen_totp(grab(res_logged, "totp_secret")),
        },
        expected_code=200,
    )

    assrt_msg(res_totp, "verification successful")

    res_new_pwd = await wrap_httpx(
        api,
        url="/auth/recover-pwd-2FA",
        expected_code=200,
        data={
            "password": gen_pwd(5),
            "cbc_hmac_token": grab(res_verify, "cbc_hmac_token"),
        },
        method="PATCH",
    )

    assert REG_JWT.fullmatch(grab(res_new_pwd, "access_token"))
    assert REG_JWE.fullmatch(res_new_pwd["refresh_token"])

    assrt_msg(res_new_pwd, "password updated")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("totp_wrong", 401, "totp_code_invalid"),
        ("cbc_hmac_expired", 401, "cbc_hmac_expired"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    res_logged = await get_us_2FA_lib(api, cbc_hmac_t=TokenT.RECOVER_PWD)

    res_verify = await wrap_httpx(
        api,
        url=f"/verify/recover-pwd?cbc_hmac_token={res_logged['cbc_hmac_token']}",  # noqa: E501
        method="GET",
        expected_code=200,
    )

    token_2FA = grab(res_verify, "cbc_hmac_token")
    get_aad_cbc_hmac(token_2FA, TokenT.RECOVER_PWD_2FA)

    if case == "cbc_hmac_expired":
        token_2FA = (
            await get_tokens_lib(
                api,
                existing_payload=res_logged["payload"],
                expired=["cbc_hmac"],
                cbc_hmac_t=TokenT.RECOVER_PWD_2FA,
            )
        )["cbc_hmac_token"]

    res_totp = await wrap_httpx(
        api,
        url="/verify/recover-pwd-2FA-totp",
        expected_code=expected_code,
        data={
            "cbc_hmac_token": token_2FA,
            "totp_code": (
                "123456"
                if case == "totp_wrong"
                else gen_totp(
                    totp_secret=grab(
                        res_logged, "totp_secret", exclude_parents=["user"]
                    )
                )
            ),
        },
    )

    assrt_msg(res_totp, expected_msg)
