from httpx import AsyncClient
import pytest

from src.__dev_only.payloads import (
    gen_payload_application_client,
)
from src.constants.reg import REG_ID
from tests.conf.lib.etc import get_tokens_lib
from tests.conf.lib.idx import wrap_httpx

relevant_keys = [
    "company_name",
    "position_name",
    "status",
]


@pytest.mark.asyncio
async def ok_t(api: AsyncClient) -> None:
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

    for k in relevant_keys:
        assert res_post["data"]["job_application"][k] == original_payload[k]

    assert REG_ID.fullmatch(appl_id)

    updated_payload = gen_payload_application_client()
    res_put = await wrap_httpx(
        api,
        url=f"/job-applications/{appl_id}",
        method="PUT",
        expected_code=200,
        data=updated_payload,
        access_token=res["access_token"],
    )

    assert res_put["data"]["job_application"]["id"] == appl_id

    for k in relevant_keys:
        assert res_put["data"]["job_application"][k] == updated_payload[k]
