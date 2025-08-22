from typing import TypedDict
from fastapi import Request
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.tokens.cbc_hmac import check_cbc_hmac
from src.models.token import CheckTokenReturnT, TokenT


class ActionAccountMdwReturnT(TypedDict):
    result_cbc_hmac: CheckTokenReturnT
    body: dict[str, str]


async def action_account_mdw(req: Request) -> ActionAccountMdwReturnT:
    bd: dict | None = None

    try:
        bd = await req.json()
    except Exception:
        ...

    if not bd:
        raise ErrAPI(msg="Invalid data format", status=422)

    async with db_trx() as trx:
        result_cbc_hmac: CheckTokenReturnT = await check_cbc_hmac(
            trx=trx, token_t=TokenT.MANAGE_ACC, token=bd["cbc_hmac_token"]
        )

        return {"result_cbc_hmac": result_cbc_hmac, "body": bd}
