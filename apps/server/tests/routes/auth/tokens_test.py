from httpx import AsyncClient
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


@pytest.mark.asyncio
async def checkExpired_t(api: AsyncClient) -> None:
    res_expired = await api.post("/test/tokens-expired", json=PAYLOAD_REGISTER)

    data = parse_res(res_expired)
    assert data["access_token"] and data["refresh_token"] and data["cbc_hmac"]

    url: str = "/test/get-err-expired"

    res_jwt = await api.post(
        url,
        json={"token": data["access_token"], "act": "JWT"},
    )
    data_jwt = parse_res(res_jwt)

    assert res_jwt.status_code == 401
    assert "ACCESS_TOKEN_EXPIRED" in data_jwt["msg"]

    res_jwe = await api.post(
        url,
        json={"token": data["refresh_token"], "act": "JWE"},
    )
    data_jwe = parse_res(res_jwe)

    assert res_jwe.status_code == 401
    assert "REFRESH_TOKEN_EXPIRED" in data_jwe["msg"]
