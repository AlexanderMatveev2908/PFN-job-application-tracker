from typing import Awaitable, Callable
from fastapi import Request
from src.conf.db import db_trx
from src.lib.tokens.cbc_hmac import check_cbc_hmac_with_us
from src.models.token import CheckTokenWithUsReturnT, TokenT


def check_cbc_hmac_mdw(
    token_t: TokenT,
) -> Callable[[Request], Awaitable[CheckTokenWithUsReturnT]]:

    async def _check_cbc(req: Request) -> CheckTokenWithUsReturnT:
        token = req.query_params.get("cbc_hmac_token", None)

        async with db_trx() as trx:
            return await check_cbc_hmac_with_us(
                token=token, trx=trx, token_t=token_t
            )

    return _check_cbc
