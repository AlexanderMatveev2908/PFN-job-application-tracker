import pytest
from src.__dev_only.payloads import RegisterPayloadT, get_payload_register
from tests.conf.lib.etc import register_ok_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient
from typing import Callable

URL = "/auth/register"


@pytest.mark.asyncio
async def test_register_ok(api: AsyncClient) -> None:
    await register_ok_lib(api)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "gen_payload, expected_code, expected_msg",
    [
        (
            lambda: get_payload_register(),
            409,
            "user already exists",
        ),
        (
            lambda: {
                **get_payload_register(),
                "confirm_password": "totally_wrong_password",
            },
            422,
            "passwords do not match",
        ),
        (
            lambda: {
                **get_payload_register(),
                "terms": False,
            },
            422,
            "user must accept terms",
        ),
    ],
)
async def test_register_invalid_cases(
    api: AsyncClient,
    gen_payload: Callable[[], RegisterPayloadT],
    expected_code: int,
    expected_msg: str,
) -> None:
    payload = gen_payload()

    if expected_code == 409:
        await wrap_httpx(api, url=URL, data=payload, expected_code=201)

    res = await wrap_httpx(
        api, url=URL, data=payload, expected_code=expected_code
    )
    assert expected_msg in res["data"]["msg"].lower()


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
