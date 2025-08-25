from httpx import AsyncClient
import pytest

from src.constants.reg import REG_SECRET_TOTP
from tests.conf.lib.etc import gen_verified_user_lib
from tests.conf.lib.idx import wrap_httpx

URL = "/user/2FA"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res = await gen_verified_user_lib(api)

    res_2FA = await wrap_httpx(
        api,
        url=URL,
        method="PATCH",
        access_token=res["access_token"],
        data={"cbc_hmac_token": res["cbc_hmac_token"]},
        expected_code=200,
    )

    assert REG_SECRET_TOTP.fullmatch(res_2FA["data"]["totp_secret"])

    assert len(res_2FA["data"]["backup_codes"]) == 8


@pytest.mark.asyncio
@pytest.mark.parametrize("case, expected_code, expected_msg", [])
async def bad_cases_t(
    api: AsyncClient, case, expected_code, expected_msg
) -> None: ...
