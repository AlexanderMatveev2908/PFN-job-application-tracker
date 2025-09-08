from typing import Any, cast
from httpx import AsyncClient
import pytest

from src.__dev_only.payloads import gen_job_appl_payload
from src.constants.reg import REG_ID
from tests.conf.lib.data_structure import assrt_msg
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
    res_tokens = await get_tokens_lib(
        api,
    )

    payload = gen_job_appl_payload(res_tokens["user"]["id"])
    files = {k: (None, str(v)) for k, v in payload.items()}

    res_post = await wrap_httpx(
        api,
        url="/job-applications/",
        expected_code=201,
        access_token=res_tokens["access_token"],
        files=files,
    )

    assert REG_ID.fullmatch(res_post["data"]["job_application"]["id"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case, expected_code, expected_msg",
    [
        ("jwt_not_provided", 401, "jwt_not_provided"),
        ("jwt_expired", 401, "jwt_expired"),
        ("miss_data", 422, "wrong data format"),
        ("err_status", 422, None),
        ("err_date", 422, None),
        ("err_name", 422, None),
    ],
)
async def bad_cases_t(
    api: AsyncClient, case: str, expected_code: int, expected_msg: str
) -> None:
    res_tokens = await get_tokens_lib(api, expired=case.split("_expired"))

    payload = gen_job_appl_payload(res_tokens["user"]["id"])
    if case == "err_status":
        payload["status"] = cast(Any, "wrong_status")
    elif case == "err_date":
        payload["date_applied"] = cast(Any, "1234")
    elif case == "err_name":
        payload["company_name"] = "<script>"

    files = {k: (None, str(v)) for k, v in payload.items()}

    res_post = await wrap_httpx(
        api,
        url="/job-applications/",
        expected_code=expected_code,
        access_token=(
            res_tokens["access_token"] if case != "jwt_not_provided" else ""
        ),
        files=files if case != "miss_data" else None,
    )

    if expected_msg:
        assrt_msg(res_post, expected_msg)
