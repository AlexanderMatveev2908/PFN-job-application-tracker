from typing import Any, Awaitable, Callable, Type, TypeVar, TypedDict, cast

from fastapi import Request
from pydantic import BaseModel

from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.tokens.cbc_hmac import check_cbc_hmac_with_us
from src.middleware.check_form import check_form_mdw
from src.middleware.check_jwt import check_jwt_mdw
from src.models.token import CheckTokenWithUsReturnT, TokenT


FormT = TypeVar("FormT", bound=BaseModel)


class ComboCheckJwtCbcReturnT(TypedDict):
    cbc_hmac_result: CheckTokenWithUsReturnT


class ComboCheckJwtCbcBodyReturnT(ComboCheckJwtCbcReturnT):
    body: dict[str, Any]


ComboCheckJwtCbcReturnAlsT = (
    ComboCheckJwtCbcReturnT | ComboCheckJwtCbcBodyReturnT
)


def combo_check_bd_jwt_bcb_hmac_mdw(
    token_t: TokenT,
    check_jwt: bool,
    model: Type[FormT] | None = None,
) -> Callable[
    [Request],
    Awaitable[ComboCheckJwtCbcReturnAlsT],
]:

    async def _check(
        req: Request,
    ) -> ComboCheckJwtCbcReturnAlsT:
        if check_jwt:
            check_jwt_mdw(req)

        data: dict | None = None

        is_body = model and issubclass(model, BaseModel)

        if is_body:
            try:
                data = await req.json()
            except Exception:
                ...

            if not data:
                raise ErrAPI(msg="wrong data format", status=422)

            token: str | None = data.get("cbc_hmac_token")
        else:
            token = req.query_params.get("cbc_hmac_token")

        async with db_trx() as trx:
            result_cbc_hmac = await check_cbc_hmac_with_us(
                token=token, trx=trx, token_t=token_t
            )

            if is_body:
                await check_form_mdw(model=cast(Type[FormT], model), data=data)

            result = {"body": data, "cbc_hmac_result": result_cbc_hmac}

            if is_body:
                return cast(ComboCheckJwtCbcBodyReturnT, result)
            else:
                return cast(ComboCheckJwtCbcReturnT, result)

    return _check
