import pytest
from src.__dev_only.payloads import RegisterPayloadT, get_payload_register
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient
from typing import Callable

from tests.conf.lib.register import register_ok_lib

URL = "/auth/register"


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
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
async def bad_cases_t(
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
    assrt_msg(res, expected_msg)
