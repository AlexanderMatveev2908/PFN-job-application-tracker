from httpx import AsyncClient
import pytest

from src.constants.reg import REG_JWE, REG_JWT
from src.lib.pwd_gen import gen_pwd
from src.models.token import TokenT
from tests.conf.lib import get_tokens_lib, wrap_httpx

URL = "/auth/recover-pwd"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(
        api,
        cbc_hmac_t=TokenT.RECOVER_PWD,
    )

    new_pwd = gen_pwd(n=5)

    res_change = await wrap_httpx(
        api,
        url=URL,
        data={
            "cbc_hmac_token": res_tokens["cbc_hmac_token"],
            "new_password": new_pwd,
        },
        expected_code=200,
    )

    assert REG_JWT.fullmatch(res_change["data"]["access_token"])
    assert REG_JWE.fullmatch(res_change["refresh_token"])
    assert "password updated" in res_change["data"]["msg"]
