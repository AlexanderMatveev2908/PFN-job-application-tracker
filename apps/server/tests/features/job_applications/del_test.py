from httpx import AsyncClient
import pytest

from src.__dev_only.payloads import gen_payload_application_client
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx


async def common_cb(api: AsyncClient) -> tuple:
    res_tokens = await get_tokens_lib(api)

    res_post = await wrap_httpx(
        api,
        url="/job-applications",
        access_token=res_tokens["access_token"],
        data=gen_payload_application_client(),
        expected_code=201,
    )

    application_id_post = res_post["data"]["job_application"]["id"]

    url = f"/job-applications/{application_id_post}"

    res_get = await wrap_httpx(
        api,
        url=url,
        access_token=res_tokens["access_token"],
        expected_code=200,
        method="GET",
    )

    assert res_get["data"]["application"]["id"] == application_id_post

    return (res_tokens, url, application_id_post)


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:

    (res_tokens, url, *_) = await common_cb(api)

    await wrap_httpx(
        api,
        url=url,
        expected_code=200,
        method="DELETE",
        access_token=res_tokens["access_token"],
    )

    res_get_after_del = await wrap_httpx(
        api,
        url=url,
        access_token=res_tokens["access_token"],
        expected_code=404,
        method="GET",
    )

    assrt_msg(res_get_after_del, "application not found")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("jwt_not_provided", 401, "jwt_not_provided"),
        ("jwt_expired", 401, "jwt_expired"),
        ("wrong_id", 422, None),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:

    res_tokens, url, application_id_post = await common_cb(api)

    access_token = res_tokens["access_token"]

    if case == "jwt_not_provided":
        access_token = ""
    elif case == "jwt_expired":
        access_token = (
            await get_tokens_lib(
                api, existing_payload=res_tokens["payload"], expired=["jwt"]
            )
        )["access_token"]

    res_del = await wrap_httpx(
        api,
        url=url if case != "wrong_id" else "/job-applications/w222jf",
        expected_code=expected_code,
        method="DELETE",
        access_token=access_token,
    )

    if expected_msg:
        assrt_msg(res_del, expected_msg)

    res_get_after_fail_del = await wrap_httpx(
        api,
        url=url,
        access_token=res_tokens["access_token"],
        expected_code=200,
        method="GET",
    )

    assert (
        res_get_after_fail_del["data"]["application"]["id"]
        == application_id_post
    )
