from fastapi import Request

from src.conf.db import db_trx
from src.lib.tokens.cbc_hmac import check_cbc_hmac
from src.middleware.check_jwt import check_jwt_mdw
from src.models.token import CheckTokenReturnT, TokenT


async def action_account_mdw(req: Request, token: str) -> CheckTokenReturnT:
    check_jwt_mdw(req)

    async with db_trx() as trx:
        result_cbc_hmac: CheckTokenReturnT = await check_cbc_hmac(
            trx=trx, token_t=TokenT.MANAGE_ACC, token=token
        )

        return result_cbc_hmac
