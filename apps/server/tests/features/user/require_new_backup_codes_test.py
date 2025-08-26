from typing import cast
from httpx import AsyncClient
import pytest

from src.constants.reg import REG_JWT
from src.lib.etc import grab
from src.models.token import TokenT
from tests.conf.lib.data_structure import (
    extract_login_payload,
    gen_totp,
    get_aad_cbc_hmac,
)
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.login import get_logged_2fa


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_logged = await get_logged_2fa(api)

    for i in range(8):
        res_login_0 = await wrap_httpx(
            api,
            url="/auth/login",
            expected_code=200,
            data=extract_login_payload(res_logged["payload"]),
        )

        token_login = cast(str, grab(res_login_0, "cbc_hmac_token"))
        get_aad_cbc_hmac(
            token=token_login,
            token_t=TokenT.LOGIN_2FA,
        )

        res_login1 = await wrap_httpx(
            api,
            url="/auth/login-2FA-backup-code",
            expected_code=200,
            data={
                "cbc_hmac_token": token_login,
                "backup_code": cast(
                    list[str], grab(res_logged, "backup_codes")
                )[i],
            },
        )

        access_token: str = cast(str, grab(res_login1, "access_token"))
        assert REG_JWT.fullmatch(access_token)
        assert grab(res_login1, "backup_codes_left") == (
            len(cast(list, grab(res_logged, "backup_codes"))) - (i + 1)
        )

    res_tokens = await get_tokens_lib(
        api,
        existing_payload=res_logged["payload"],
    )

    access_token = res_tokens["access_token"]

    res_manage_0 = await wrap_httpx(
        api,
        url="/user/manage-account",
        access_token=access_token,
        expected_code=200,
        data={"password": grab(res_logged, "password", parent="payload")},
    )

    res_manage_1 = await wrap_httpx(
        api,
        url="/user/manage-account-2FA-totp",
        access_token=access_token,
        expected_code=200,
        data={
            "cbc_hmac_token": grab(res_manage_0, "cbc_hmac_token"),
            "totp_code": gen_totp(res_logged["totp_secret"]),
        },
    )

    res_new_codes = await wrap_httpx(
        api,
        url="/user/new-backup-codes",
        access_token=access_token,
        expected_code=200,
        data={"" "cbc_hmac_token": grab(res_manage_1, "cbc_hmac_token")},
    )

    codes = grab(res_new_codes, "backup_codes")
    assert isinstance(codes, list)
    assert len(codes) == 8
