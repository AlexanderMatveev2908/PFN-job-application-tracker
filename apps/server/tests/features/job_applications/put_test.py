from httpx import AsyncClient
import pytest

from src.__dev_only.payloads import (
    gen_payload_application_client,
)
from src.constants.reg import REG_ID
from src.lib.data_structure.etc import pack
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx

relevant_keys = [
    "company_name",
    "position_name",
    "status",
]


async def common_cb(api: AsyncClient) -> dict:
    res = await get_tokens_lib(api)

    original_payload = gen_payload_application_client()
    res_post = await wrap_httpx(
        api,
        url="/job-applications",
        expected_code=201,
        data=original_payload,
        access_token=res["access_token"],
    )

    appl_id = res_post["data"]["job_application"]["id"]
    assert REG_ID.fullmatch(appl_id)

    for k in relevant_keys:
        assert res_post["data"]["job_application"][k] == original_payload[k]

    updated_payload = gen_payload_application_client()  # noqa

    return pack("updated_payload", "appl_id", "res")

    # return {
    #     n: locals()[n] for n in ("updated_payload", "appl_id", "access_token") # noqa: E501
    # }


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:

    result = await common_cb(api)

    res_put = await wrap_httpx(
        api,
        url=f"/job-applications/{result["appl_id"]}",
        method="PUT",
        expected_code=200,
        data=result["updated_payload"],
        access_token=result["res"]["access_token"],
    )

    assert res_put["data"]["job_application"]["id"] == result["appl_id"]

    for k in relevant_keys:
        assert (
            res_put["data"]["job_application"][k]
            == result["updated_payload"][k]
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("jwt_not_provided", 401, "jwt_not_provided"),
        ("jwt_expired", 401, "jwt_expired"),
        ("invalid_payload", 422, None),
        ("id_invalid", 422, None),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    result = await common_cb(api)

    updated_payload = result["updated_payload"]

    access_token = result["res"]["access_token"]
    if case == "jwt_expired":
        access_token = (
            await get_tokens_lib(
                api, existing_payload=result["res"]["payload"], expired=["jwt"]
            )
        )["access_token"]
    elif case == "jwt_not_provided":
        access_token = ""

    if case == "invalid_payload":
        updated_payload["company_name"] = "<>✌🏼<>/;%$#"

    res_put = await wrap_httpx(
        api,
        url=f"/job-applications/{result["appl_id"] if case != "id_invalid" else "<><>22222"}",  # noqa: E501
        method="PUT",
        expected_code=expected_code,
        data=updated_payload,
        access_token=access_token,
    )

    if expected_msg:
        assrt_msg(res_put, expected_msg)
