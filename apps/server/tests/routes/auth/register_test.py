import pytest
from src.constants.reg import REG_CBC_HMAC, REG_JWE, REG_JWT
from src.lib.logger import clg
from tests.routes.auth.constants import PAYLOAD_REGISTER


@pytest.mark.asyncio
async def register_ok_t(api) -> None:

    res = await api.post("/auth/register", json=PAYLOAD_REGISTER)

    data = res.json()

    clg(data, res.cookies, ttl=f"🚦 => {res.status_code}")

    assert res.status_code == 200
    assert "new_user" in data
    assert REG_JWT.fullmatch(data["access_token"])
    assert REG_JWE.fullmatch(res.cookies["refresh_token"])
    assert REG_CBC_HMAC.fullmatch(data["cbc_hmac_token"])
    assert data["new_user"]["email"] == PAYLOAD_REGISTER["email"]


@pytest.mark.asyncio
async def register_err_existing_t(api) -> None:

    # _ expect all good as above
    res_0 = await api.post("/auth/register", json=PAYLOAD_REGISTER)
    data_0 = res_0.json()

    clg(data_0, ttl=f"🚦 => {res_0.status_code}")

    assert res_0.status_code == 200
    assert "new_user" in data_0
    assert data_0["new_user"]["email"] == PAYLOAD_REGISTER["email"]

    # ! expect crash
    res_1 = await api.post("/auth/register", json=PAYLOAD_REGISTER)
    data_1 = res_1.json()

    clg(data_1, ttl=f"🚦 => {res_1.status_code}")

    assert res_1.status_code == 409
    assert "user already exists" in data_1["msg"]


@pytest.mark.asyncio
async def register_err_mismatch_t(api) -> None:

    payload = {
        **PAYLOAD_REGISTER,
        "confirm_password": "a4A0.E.H,p$VjDaw&bzX!_A#V+1P)"
        "juV2726439d_wrong_password_mismatch",
    }

    res = await api.post("/auth/register", json=payload)

    data = res.json()

    clg(data, ttl=f"🚦 => {res.status_code}")

    assert res.status_code == 422
    assert "passwords do not match" in data["msg"].lower()


@pytest.mark.asyncio
async def register_err_terms_t(api) -> None:

    payload = {
        **PAYLOAD_REGISTER,
        "terms": False,
    }

    res = await api.post("/auth/register", json=payload)

    data = res.json()

    clg(data, ttl=f"🚦 => {res.status_code}")

    assert res.status_code == 422
    assert "user must accept terms" in data["msg"].lower()


# @pytest.mark.asyncio
# async def register_err_limit_t(api) -> None:

#     payload = {
#         **PAYLOAD_REGISTER,
#         "first_name": "<>!@#$%^",
#     }

#     for _ in range(0, 10):
#         res = await api.post("/auth/register", json=payload)
#         data = res.json()

#         assert res.status_code == 422
#         assert "string should match pattern".lower() in data["msg"].lower()

#     res = await api.post("/auth/register", json=payload)
#     data = res.json()

#     clg(
#         f"🚦 => {res.status_code}",
#         data,
#         res.headers["RateLimit-Limit"],
#         res.headers["RateLimit-Remaining"],
#         res.headers["RateLimit-Window"],
#         ttl=f"🚦 => {res.status_code}",
#     )

#     assert res.status_code == 429
#     assert res.headers["RateLimit-Limit"] == "10"
#     assert res.headers["RateLimit-Remaining"] == "0"
#     assert res.headers["RateLimit-Window"] == str(1000 * 60 * 15)
#     assert int(res.headers["RateLimit-Reset"]) > 800
#     assert all(
#         h in res.headers["Access-Control-Expose-Headers"]
#         for h in [
#             "RateLimit-Limit",
#             "RateLimit-Remaining",
#             "RateLimit-Window",
#             "RateLimit-Reset",
#         ]
#     )

#     assert (
#         "Our hamster-powered server took a break".lower()
#         in data["msg"].lower()
#     )
