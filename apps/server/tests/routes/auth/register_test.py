import pytest
from src.lib.logger import clg


def_payload = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "a4A0.E.H,p$VjDaw&bzX!_A#V+1P)juV2726439d",
    "confirm_password": "a4A0.E.H,p$VjDaw&bzX!_A#V+1P)juV2726439d",
    "terms": True,
}


@pytest.mark.asyncio
async def register_ok_t(api) -> None:

    res = await api.post("/auth/register", json=def_payload)

    data = res.json()

    clg(f"🚦 => {res.status_code}", data, ttl="res")

    assert res.status_code == 200
    assert "new_user" in data
    assert data["new_user"]["email"] == def_payload["email"]


@pytest.mark.asyncio
async def register_err_existing_t(api) -> None:

    # _ expect all good as above
    res_0 = await api.post("/auth/register", json=def_payload)
    data_0 = res_0.json()

    clg(f"🚦 => {res_0.status_code}", data_0, ttl="res")

    assert res_0.status_code == 200
    assert "new_user" in data_0
    assert data_0["new_user"]["email"] == def_payload["email"]

    # ! expect crash
    res_1 = await api.post("/auth/register", json=def_payload)
    data_1 = res_1.json()

    clg(f"🚦 => {res_1.status_code}", data_1, ttl="res")

    assert res_1.status_code == 409
    assert "user already exists" in data_1["msg"]


@pytest.mark.asyncio
async def register_err_mismatch_t(api) -> None:

    payload = {
        **def_payload,
        "confirm_password": "a4A0.E.H,p$VjDaw&bzX!_A#V+1P)"
        "juV2726439d_wrong_password_mismatch",
    }

    res = await api.post("/auth/register", json=payload)

    data = res.json()

    clg(f"🚦 => {res.status_code}", data, ttl="res")

    assert res.status_code == 422
    assert "passwords do not match" in data["msg"].lower()


@pytest.mark.asyncio
async def register_err_terms_t(api) -> None:

    payload = {
        **def_payload,
        "terms": False,
    }

    res = await api.post("/auth/register", json=payload)

    data = res.json()

    clg(f"🚦 => {res.status_code}", data, ttl="res")

    assert res.status_code == 422
    assert "user must accept terms" in data["msg"].lower()


# @pytest.mark.asyncio
# async def register_err_limit_t(api) -> None:

#     payload = {
#         **def_payload,
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
#         ttl="res",
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
