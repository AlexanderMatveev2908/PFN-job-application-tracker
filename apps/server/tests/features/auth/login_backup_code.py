from httpx import AsyncClient
import pytest

from src.constants.reg import REG_CBC_HMAC, REG_JWT
from tests.conf.lib.data_structure import extract_login_payload
from tests.conf.lib.etc import get_us_2FA
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    us_2fa = await get_us_2FA(
        api,
    )

    res_login = await wrap_httpx(
        api,
        url="/auth/login",
        data=extract_login_payload(us_2fa["payload"]),
        expected_code=200,
    )

    assert REG_CBC_HMAC.fullmatch(res_login["data"]["cbc_hmac_token"])

    res_login_2fa = await wrap_httpx(
        api,
        url="/auth/login-backup-code",
        expected_code=200,
        data={
            "cbc_hmac_token": res_login["data"]["cbc_hmac_token"],
            "backup_code": us_2fa["backup_codes"][0],
        },
    )

    assert REG_JWT.fullmatch(res_login_2fa["data"]["access_token"])
    assert res_login_2fa["data"]["backup_codes_left"] == 7
