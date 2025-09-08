from httpx import AsyncClient
import pytest

from src.__dev_only.payloads import gen_job_appl_payload
from src.constants.reg import REG_ID
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
