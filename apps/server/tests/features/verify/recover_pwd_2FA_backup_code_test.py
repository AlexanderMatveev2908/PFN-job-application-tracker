from httpx import AsyncClient
import pytest

from src.lib.etc import grab
from src.lib.pwd_gen import gen_pwd
from src.models.token import TokenT
from tests.conf.lib.data_structure import (
    assrt_sessions_tokens,
    get_aad_cbc_hmac,
)
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.get_us import get_us_2FA_lib
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_logged = await get_us_2FA_lib(api)

    res_tokens = await get_tokens_lib(
        api,
        existing_payload=res_logged["payload"],
        cbc_hmac_t=TokenT.RECOVER_PWD,
    )

    res_verify = await wrap_httpx(
        api,
        url=f"/verify/recover-pwd?cbc_hmac_token={res_tokens['cbc_hmac_token']}",  # noqa: E501
        expected_code=200,
        method="GET",
    )

    token_2FA = grab(res_verify, "cbc_hmac_token")

    get_aad_cbc_hmac(token_2FA, TokenT.RECOVER_PWD_2FA)

    await wrap_httpx(
        api,
        url="/verify/recover-pwd-2FA-backup-code",
        expected_code=200,
        data={
            "cbc_hmac_token": token_2FA,
            "backup_code": res_logged["backup_codes"][0],
        },
    )

    res_new_pwd = await wrap_httpx(
        api,
        url="/auth/recover-pwd-2FA",
        data={
            "password": gen_pwd(5),
            "cbc_hmac_token": token_2FA,
        },
        method="PATCH",
    )

    assrt_sessions_tokens(res_new_pwd)
