from src.__dev_only.payloads import get_payload_register
from tests.conf.lib.data_structure import assrt_sessions_tokens
from tests.conf.lib.idx import wrap_httpx
from tests.conf.lib.types import RegisterOkLibReturnT


async def register_ok_lib(api) -> RegisterOkLibReturnT:
    payload = get_payload_register()

    res_register = await wrap_httpx(
        api,
        url="/auth/register",
        data=payload,
        expected_code=201,
    )

    assrt_sessions_tokens(res_register)

    return {
        "payload": payload,
        "access_token": res_register["data"]["access_token"],
        "refresh_token": res_register["refresh_token"],
    }
