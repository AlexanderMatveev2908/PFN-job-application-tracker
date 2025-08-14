import pytest
from src.lib.logger import clg


@pytest.mark.asyncio
async def register_ok__t(api) -> None:

    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "a4A0.E.H,p$VjDaw&bzX!_A#V+1P)juV2726439d",
        "confirm_password": "a4A0.E.H,p$VjDaw&bzX!_A#V+1P)juV2726439d",
        "terms": True,
    }

    res = await api.post("/auth/register", json=payload)

    data = res.json()

    clg(f"🚨 => {res.status_code}", data, ttl="res")

    assert res.status_code == 200
    assert "new_user" in data
    assert data["new_user"]["email"] == payload["email"]


@pytest.mark.asyncio
async def register_err__t(api) -> None:

    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "a4A0.E.H,p$VjDaw&bzX!_A#V+1P)juV2726439d",
        "confirm_password": "a4A0.E.H,p$VjDaw&bzX!_A#V+1P)"
        "juV2726439d_wrong_password_mismatch",
        "terms": True,
    }

    res = await api.post("/auth/register", json=payload)

    data = res.json()

    clg(f"🚨 => {res.status_code}", data, ttl="res")

    assert res.status_code == 422
    assert "passwords do not match" in data["msg"].lower()
