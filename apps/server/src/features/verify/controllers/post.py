from fastapi import Depends, Request
from sqlalchemy import delete, false, select
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

        stmt_find = select(User).where(
            (User.id == cbc_result["decrypted"]["user_id"])
            & (User.is_verified == false())
        )
        us = (await trx.execute(stmt_find)).scalars().one_or_none()

        if not us:
            raise ErrAPI(msg="user not found", status=404)

        us.verify_email()
        stmt_del = delete(Token).where(Token.id == cbc_result["token_d"]["id"])
        await trx.execute(stmt_del)

        return ResAPI.ok_200(updated_user=us.to_d(exclude_keys=["password"]))


async def forgot_pwd_ctrl(req: Request) -> ResAPI:
    return ResAPI.ok_200()
