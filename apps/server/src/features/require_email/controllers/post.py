from fastapi import Depends, Request
from src.conf.db import db_trx
from src.conf.env import get_env
from src.decorators.res import ResAPI
from src.features.require_email.middleware.require_email import (
    require_email_mdw,
)
from src.lib.emails.aiosmtp.idx import send_email
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.models.token import TokenT
from src.models.user import UserDcT


async def require_email_forgot_pwd_ctrl(
    _: Request,
    user: UserDcT = Depends(require_email_mdw),
) -> ResAPI:

    async with db_trx() as trx:

        cbc_hmac_result = await gen_cbc_hmac(
            user_id=user["id"], trx=trx, hdr={"token_t": TokenT.RECOVER_PWD}
        )

        if get_env().py_env != "test":
            await send_email(
                callback_url=f"https://pfn-job-application-tracker-client.fly.dev?cbc_hmac_token={cbc_hmac_result['client_token']}",  # noqa: E501
                subj="RECOVER PASSWORD 🔒",
                user=user,
            )

    return ResAPI.ok_201(msg="📮 email sent")


async def confirm_email_ctrl(
    _: Request,
    user: UserDcT = Depends(require_email_mdw),
) -> ResAPI:
    return ResAPI.ok_200(msg="📮 email sent")
