import pytest
from src.lib.etc import grab
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg, get_aad_cbc_hmac
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient

URL = "/verify/confirm-email?cbc_hmac_token="


@pytest.mark.asyncio
async def ok_t(api) -> None:
    res_register = await get_tokens_lib(api)

    res_conf = await wrap_httpx(
        api,
        method="GET",
        url=f'{URL}{res_register["cbc_hmac_token"]}',
        expected_code=200,
    )

    assert grab(res_conf, "is_verified") is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("already_verified", 409, "user already verified"),
        ("expired", 401, "cbc_hmac_expired"),
        ("invalid", 401, "cbc_hmac_invalid"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    url = ""

    if case == "already_verified":
        res_register = await get_tokens_lib(api)

        res_conf = await wrap_httpx(
            api,
            method="GET",
            url=f'{URL}{res_register["cbc_hmac_token"]}',
            expected_code=200,
        )
        assert grab(res_conf, "is_verified") is True

        res_tokens = await get_tokens_lib(
            api, existing_payload=res_register["payload"]
        )

        parsed = get_aad_cbc_hmac(
            token=res_tokens["cbc_hmac_token"], token_t=TokenT.CONF_EMAIL
        )
        assert parsed["user_id"] == grab(res_conf, "id", parent="updated_user")

        url = f'{URL}{res_tokens["cbc_hmac_token"]}'

    elif case == "expired":
        res_tokens = await get_tokens_lib(api, reverse=True)
        url = f"{URL}{res_tokens['cbc_hmac_token']}"

    elif case == "invalid":
        res_tokens = await get_tokens_lib(api, reverse=True)
        url = f"{URL}{res_tokens['cbc_hmac_token'][:-4]}afaf"

    res_conf = await wrap_httpx(
        api, method="GET", url=url, expected_code=expected_code
    )

    assrt_msg(res_conf, expected_msg)
