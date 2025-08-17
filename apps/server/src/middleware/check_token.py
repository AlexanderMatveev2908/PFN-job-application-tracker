from fastapi import Request
from src.conf.db import db_trx
from src.constants.reg import REG_CBC_HMAC
from src.decorators.err import ErrAPI
from src.lib.tokens.cbc_hmac import check_cbc_hmac
from src.models.token import CheckTokenReturnT


async def check_cbc_hmac_mdw(req: Request) -> CheckTokenReturnT:
    token = req.query_params.get("cbc_hmac_token", None)

    if not token:
        raise ErrAPI(msg="CBC_HMAC_NOT_PROVIDED", status=401)

    if not REG_CBC_HMAC.fullmatch(token):
        raise ErrAPI(msg="CBC_HMAC_INVALID_FORMAT", status=401)

    async with db_trx() as trx:
        return await check_cbc_hmac(token, trx)
