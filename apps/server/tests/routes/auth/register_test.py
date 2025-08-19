import pytest
from tests.conf.lib import register_ok_lib, wrap_httpx
from tests.conf.constants import get_payload_register

URL = "/auth/register"


@pytest.mark.asyncio
async def ok_t(api) -> None:

    await register_ok_lib(api)


@pytest.mark.asyncio
async def err_existing_t(api) -> None:
    # _ First call: should succeed
    res_register = await register_ok_lib(api)

    # ! Second call: same payload → conflict
    res_register_err = await wrap_httpx(
        api,
        url=URL,
        data=res_register["payload"],
        expected_code=409,
    )
    assert "user already exists" in res_register_err["data"]["msg"].lower()


@pytest.mark.asyncio
async def err_mismatch_t(api) -> None:
    payload = {
        **get_payload_register(),
        "confirm_password": (
            "a4A0.E.H,p$VjDaw&bzX!_A#V+1P)juV2726439d_wrong_password_mismatch"
        ),
    }

    res_register = await wrap_httpx(
        api,
        url=URL,
        data=payload,
        expected_code=422,
    )
    assert "passwords do not match" in res_register["data"]["msg"].lower()


@pytest.mark.asyncio
async def err_terms_t(api) -> None:
    payload = {**get_payload_register(), "terms": False}

    res_register = await wrap_httpx(
        api,
        url=URL,
        data=payload,
        expected_code=422,
    )
    assert "user must accept terms" in res_register["data"]["msg"].lower()


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
