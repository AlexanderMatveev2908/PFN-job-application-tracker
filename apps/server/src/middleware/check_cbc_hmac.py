from typing import Any, Awaitable, Callable, Type, TypeVar, TypedDict, cast
from fastapi import Request
from pydantic import BaseModel
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.tokens.cbc_hmac import check_cbc_hmac
from src.lib.validators.idx import CbcHmacFormT
from src.middleware.check_form import check_form_mdw
from src.models.token import CheckTokenReturnT, TokenT

FormT = TypeVar("FormT", bound=BaseModel)


def check_cbc_hmac_mdw(
    token_t: TokenT,
) -> Callable[[Request], Awaitable[CheckTokenReturnT]]:

    async def _check_cbc(req: Request) -> CheckTokenReturnT:
        token = req.query_params.get("cbc_hmac_token", None)

        CbcHmacFormT(cbc_hmac_token=token)

        async with db_trx() as trx:
            return await check_cbc_hmac(cast(str, token), trx, token_t=token_t)

    return _check_cbc


class CheckReqCbcHmacMdwReturnT(TypedDict):
    body: dict[str, Any]
    cbc_hmac_result: CheckTokenReturnT


def check_req_and_cbc_hmac_mdw(
    model: Type[FormT], token_t: TokenT
) -> Callable[[Request], Awaitable[CheckReqCbcHmacMdwReturnT]]:

    async def _check(req: Request) -> CheckReqCbcHmacMdwReturnT:
        bd: dict | None = None

        try:
            bd = await req.json()
        except Exception:
            ...

        if not bd:
            raise ErrAPI(msg="Invalid data format", status=422)

        async with db_trx() as trx:
            result_cbc_hmac = await check_cbc_hmac(
                token=bd["cbc_hmac_token"], trx=trx, token_t=token_t
            )

            await check_form_mdw(model=model, data=bd)

            return {"body": bd, "cbc_hmac_result": result_cbc_hmac}

    return _check
