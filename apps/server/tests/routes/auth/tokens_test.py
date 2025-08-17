import pytest

from src.constants.reg import REG_CBC_HMAC, REG_ID, REG_JWE, REG_JWT
from tests.conf.lib import parse_res
from tests.routes.auth.constants import PAYLOAD_REGISTER


@pytest.mark.asyncio
async def tokens_health_t(api) -> None:
    res = await api.post("/test/tokens-health", json=PAYLOAD_REGISTER)

    data = parse_res(res)

    assert REG_JWT.fullmatch(data["access_token"])
    assert REG_ID.fullmatch(data["access_token_decoded"]["user_id"])

    assert REG_JWE.fullmatch(data["refresh_token"])
    assert REG_ID.fullmatch(data["refresh_token_db"]["user_id"])
    assert REG_ID.fullmatch(data["refresh_token_decrypted"]["user_id"])

    assert REG_CBC_HMAC.fullmatch(data["cbc_hmac_token"])
    assert REG_CBC_HMAC.fullmatch(data["cbc_hmac_token"])
    assert REG_ID.fullmatch(data["cbc_hmac_db"]["user_id"])
    assert REG_ID.fullmatch(data["cbc_hmac_decrypted"]["user_id"])

    assert (
        data["cbc_hmac_decrypted"]["user_id"]
        == data["refresh_token_decrypted"]["user_id"]
        == data["access_token_decoded"]["user_id"]
    )
