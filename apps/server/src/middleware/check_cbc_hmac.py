from typing import Awaitable, Callable, cast
from fastapi import Request
from src.conf.db import db_trx
from src.lib.tokens.cbc_hmac import check_cbc_hmac
from src.lib.validators.idx import CbcHmacFormT
from src.models.token import CheckTokenReturnT, TokenT


def check_cbc_hmac_mdw(
    token_t: TokenT,
) -> Callable[[Request], Awaitable[CheckTokenReturnT]]:

    async def _check_cbc(req: Request) -> CheckTokenReturnT:
        token = req.query_params.get("cbc_hmac_token", None)

        CbcHmacFormT(cbc_hmac_token=token)

        async with db_trx(auto_commit=False) as trx:
            return await check_cbc_hmac(
                cast(str, token), trx, delete_expired=True, token_t=token_t
            )

    return _check_cbc
