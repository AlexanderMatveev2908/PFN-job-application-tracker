import pytest
from src.constants.reg import REG_CBC_HMAC, REG_JWE, REG_JWT
from tests.conf.lib import wrap_httpx
from tests.conf.constants import get_payload_register


@pytest.mark.asyncio
async def register_ok_t(api) -> None:

    data, refresh_token = await wrap_httpx(
        api,
        data=get_payload_register(),
        url="/auth/register",
        expected_code=201,
    )

    assert "new_user" in data
    assert REG_JWT.fullmatch(data["access_token"])
    assert REG_JWE.fullmatch(refresh_token)
    assert isinstance(data["cbc_hmac_token"], str)
    assert REG_CBC_HMAC.fullmatch(data["cbc_hmac_token"])


@pytest.mark.asyncio
async def register_err_existing_t(api) -> None:
    # _ First call: should succeed
    payload = get_payload_register()
    data_0, refresh_0 = await wrap_httpx(
        api,
        url="/auth/register",
        data=payload,
        expected_code=201,
    )
    assert "new_user" in data_0
    assert isinstance(refresh_0, str)

    # ! Second call: same payload → conflict
    data_1, refresh_1 = await wrap_httpx(
        api,
        url="/auth/register",
        data=payload,
        expected_code=409,
    )
    assert "user already exists" in data_1.get("msg", "").lower()
    assert isinstance(refresh_1, str)  # likely "N/A" per wrapper


@pytest.mark.asyncio
async def register_err_mismatch_t(api) -> None:
    payload = {
        **get_payload_register(),
        "confirm_password": (
            "a4A0.E.H,p$VjDaw&bzX!_A#V+1P)juV2726439d_wrong_password_mismatch"
        ),
    }

    data, refresh = await wrap_httpx(
        api,
        url="/auth/register",
        data=payload,
        expected_code=422,
    )
    assert "passwords do not match" in data.get("msg", "").lower()
    assert isinstance(refresh, str)


@pytest.mark.asyncio
async def register_err_terms_t(api) -> None:
    payload = {**get_payload_register(), "terms": False}

    data, refresh = await wrap_httpx(
        api,
        url="/auth/register",
        data=payload,
        expected_code=422,
    )
    assert "user must accept terms" in data.get("msg", "").lower()
    assert isinstance(refresh, str)


# @pytest.mark.asyncio
# async def register_err_limit_t(api) -> None:

#     payload = {
#         **get_payload_register(),
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
