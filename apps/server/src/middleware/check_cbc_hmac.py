from typing import Awaitable, Callable
from fastapi import Request
from src.conf.db import db_trx
from src.lib.tokens.cbc_hmac import check_cbc_hmac_lib
from src.models.token import CheckTokenReturnT, TokenT


def check_cbc_hmac_mdw(
    token_t: TokenT,
) -> Callable[[Request], Awaitable[CheckTokenReturnT]]:

    async def _check_cbc(req: Request) -> CheckTokenReturnT:
        token = req.query_params.get("cbc_hmac_token", None)

        async with db_trx() as trx:
            return await check_cbc_hmac_lib(
                token=token, trx=trx, token_t=token_t
            )

    return _check_cbc
