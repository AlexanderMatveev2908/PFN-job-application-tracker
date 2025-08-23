from fastapi import Depends, Request
from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.features.user.middleware.manage_account import manage_account_mdw
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.models.token import GenTokenReturnT, TokenT
from src.models.user import UserDcT


async def get_access_account_ctrl(
    req: Request, us: UserDcT = Depends(manage_account_mdw)
) -> ResAPI:

    async with db_trx() as trx:

        result_cbc: GenTokenReturnT = await gen_cbc_hmac(
            trx=trx,
            user_id=us["id"],
            token_t=TokenT.MANAGE_ACC,
        )

        return ResAPI.ok_200(
            msg="verification successful",
            cbc_hmac_token=result_cbc["client_token"],
        )


async def change_email_ctrl(req: Request) -> ResAPI:
    return ResAPI.ok_200()
