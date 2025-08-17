from fastapi import Request
from src.conf.db import db_trx
from src.constants.reg import REG_CBC_HMAC
from src.decorators.err import ErrAPI
from src.lib.etc import load_bd
from src.lib.tokens.cbc_hmac import CheckCbcHmacReturnT, check_cbc_hmac


async def check_cbc_hmac_mdw(req: Request) -> CheckCbcHmacReturnT:
    token = (await load_bd(req)).get("token", None)

    if not token:
        raise ErrAPI(msg="token not provided", status=401)

    if not REG_CBC_HMAC.fullmatch(token):
        raise ErrAPI(msg="token invalid", status=401)

    async with db_trx() as trx:
        return await check_cbc_hmac(token, trx)
