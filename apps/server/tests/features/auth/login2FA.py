from httpx import AsyncClient
import pytest

from src.constants.reg import REG_CBC_HMAC
from src.lib.data_structure import b_to_d, h_to_b
from src.models.token import TokenT
from tests.conf.lib.etc import get_user_2FA
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_2FA = await get_user_2FA(api)

    res_login = await wrap_httpx(
        api,
        url="/auth/login",
        data={
            "email": res_2FA["payload"]["email"],
            "password": res_2FA["payload"]["password"],
        },
        expected_code=200,
    )

    cbc_hmac_token: str = res_login["data"]["cbc_hmac_token"]

    assert REG_CBC_HMAC.fullmatch(cbc_hmac_token)
    assert (
        TokenT(b_to_d(h_to_b(cbc_hmac_token.split(".")[0]))["token_t"])
        == TokenT.LOGIN_2FA
    )
