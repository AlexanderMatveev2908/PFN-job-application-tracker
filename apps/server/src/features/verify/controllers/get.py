from typing import cast
from fastapi import Depends, Request
from sqlalchemy import delete
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.middleware.check_token import check_cbc_hmac_mdw
from src.models.token import CheckTokenReturnT, Token, TokenT
from src.models.user import User


async def confirm_email_ctrl(
    _: Request,
    cbc_result: CheckTokenReturnT = Depends(
        check_cbc_hmac_mdw(token_t=TokenT.CONF_EMAIL)
    ),
) -> ResAPI:

    async with db_trx() as trx:

        us_d = cbc_result["user_d"]

        if us_d["is_verified"]:
            raise ErrAPI(msg="user already verified", status=409)

        us = cast(User, await trx.get(User, us_d["id"]))

        us.verify_email()
        await trx.execute(
            delete(Token).where(Token.id == cbc_result["token_d"]["id"])
        )

        return ResAPI.ok_200(
            msg="email verified",
            updated_user=us.to_d(exclude_keys=["password"]),
        )


async def forgot_pwd_ctrl(
    _: Request,
    __: CheckTokenReturnT = Depends(
        check_cbc_hmac_mdw(token_t=TokenT.RECOVER_PWD)
    ),
) -> ResAPI:

    return ResAPI.ok_200(msg="verification successful")
