from fastapi import Depends, Request
from sqlalchemy import delete, select
from src.conf.db import db_trx
from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.require_email.middleware.require_email import (
    RequireEmailForm,
    require_email_mdw,
)
from src.lib.emails.aiosmtp.idx import send_email
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.models.token import Token, TokenT
from src.models.user import User


async def require_email_forgot_pwd_ctrl(
    _: Request,
    require_email_data: RequireEmailForm = Depends(require_email_mdw),
) -> ResAPI:

    async with db_trx() as trx:
        us = (
            await trx.execute(
                select(User).where(User.email == require_email_data.email)
            )
        ).scalar_one_or_none()

        if not us:
            raise ErrAPI(msg="user not found", status=404)

        await trx.execute(
            delete(Token).where(
                (Token.user_id == us.id)
                & (Token.token_t == TokenT.RECOVER_PWD)
            )
        )

        cbc_hmac_result = await gen_cbc_hmac(
            user_id=us.id, trx=trx, hdr={"token_t": TokenT.RECOVER_PWD}
        )

        if get_env().py_env != "test":
            await send_email(
                callback_url=f"https://pfn-job-application-tracker-client.fly.dev?cbc_hmac_token={cbc_hmac_result['client_token']}",  # noqa: E501
                subj="RECOVER PASSWORD 🔒",
                user=us,
            )

    return ResAPI.ok_201(msg="📮 email sent")
