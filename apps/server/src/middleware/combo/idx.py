from typing import Any, Awaitable, Callable, Type, TypeVar, TypedDict

from fastapi import Request
from pydantic import BaseModel

from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.tokens.cbc_hmac import check_cbc_hmac
from src.middleware.check_form import check_form_mdw
from src.middleware.check_jwt import check_jwt_mdw
from src.models.token import CheckTokenReturnT, TokenT


FormT = TypeVar("FormT", bound=BaseModel)


class ComboCheckCbJwtCbcReturnT(TypedDict):
    body: dict[str, Any]
    cbc_hmac_result: CheckTokenReturnT


def combo_check_bd_jwt_bcb_hmac_mdw(
    model: Type[FormT], token_t: TokenT, check_jwt: bool
) -> Callable[[Request], Awaitable[ComboCheckCbJwtCbcReturnT]]:

    async def _check(req: Request) -> ComboCheckCbJwtCbcReturnT:
        if check_jwt:
            check_jwt_mdw(req)

        bd: dict | None = None

        try:
            bd = await req.json()
        except Exception:
            ...

        if not bd:
            raise ErrAPI(msg="Invalid data format", status=422)

        token: str | None = bd.get("cbc_hmac_token")

        if not token:
            raise ErrAPI(msg="CBC_HMAC_NOT_PROVIDED", status=401)

        async with db_trx() as trx:
            result_cbc_hmac = await check_cbc_hmac(
                token=token, trx=trx, token_t=token_t
            )

            await check_form_mdw(model=model, data=bd)

            return {"body": bd, "cbc_hmac_result": result_cbc_hmac}

    return _check
