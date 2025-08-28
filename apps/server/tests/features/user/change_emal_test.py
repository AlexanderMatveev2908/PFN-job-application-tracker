import os
import faker
import pytest
from src.constants.reg import REG_CBC_HMAC
from src.models.token import TokenT
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx
from httpx import AsyncClient
from tests.conf.lib.register import register_ok_lib

URL = "/user/change-email"


@pytest.mark.asyncio
async def ok_t(api) -> None:
    res_register = await register_ok_lib(api)

    res_manage = await wrap_httpx(
        api,
        url="/user/manage-account",
        data={"password": res_register["payload"]["password"]},
        access_token=res_register["access_token"],
        expected_code=200,
    )
    assert REG_CBC_HMAC.fullmatch(res_manage["data"]["cbc_hmac_token"])

    new_email = os.urandom(20).hex() + "@gmail.com"

    res_mail = await wrap_httpx(
        api,
        url=URL,
        data={
            "email": new_email,
            "cbc_hmac_token": res_manage["data"]["cbc_hmac_token"],
        },
        access_token=res_register["access_token"],
        expected_code=200,
        method="PATCH",
    )

    assrt_msg(res_mail, "email sent to new address")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("invalid_jwt", 401, "jwt_invalid"),
        ("invalid_cbc", 401, "cbc_hmac_invalid"),
        ("jwt_expired", 401, "jwt_expired"),
        ("cbc_hmac_expired", 401, "cbc_hmac_expired"),
        ("same_email", 400, "new email can not be same as old one"),
        ("existing_email", 409, "user with this email already exists"),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:

    res_tk = await get_tokens_lib(
        api, cbc_hmac_t=TokenT.MANAGE_ACC, expired=case.split("_expired")
    )

    jwt = res_tk["access_token"]
    jwt = jwt[:-4] + "aaff" if case == "invalid_jwt" else jwt
    cbc_hmac = res_tk["cbc_hmac_token"]
    cbc_hmac = cbc_hmac[:-4] + "aaff" if case == "invalid_cbc" else cbc_hmac
    payload = {
        "email": faker.Faker().email(),
        "cbc_hmac_token": cbc_hmac,
    }

    if case == "existing_email":
        payload["email"] = (await get_tokens_lib(api))["payload"]["email"]
    elif case == "same_email":
        payload["email"] = res_tk["payload"]["email"]

    res = await wrap_httpx(
        api,
        url=URL,
        data=payload,
        access_token=jwt,
        expected_code=expected_code,
        method="PATCH",
    )

    assrt_msg(res, expected_msg)
