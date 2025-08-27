import faker
from httpx import AsyncClient
import pytest

from src.constants.reg import REG_JWE, REG_JWT
from src.lib.etc import grab
from src.models.token import TokenT
from tests.conf.lib.data_structure import (
    assrt_msg,
    gen_totp,
    get_aad_cbc_hmac,
)
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.get_us import get_us_with_2FA
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_logged = await get_us_with_2FA(api, cbc_hmac_t=TokenT.MANAGE_ACC)

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

    assert REG_JWT.fullmatch(res_verify_1["data"]["access_token"])
    assert REG_JWE.fullmatch(res_verify_1["refresh_token"])
