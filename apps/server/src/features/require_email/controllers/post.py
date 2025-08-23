from fastapi import Depends, Request
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.require_email.middleware.require_email import (
    require_email_mdw,
)
from src.features.require_email.services.combo import gen_token_send_email_svc
from src.models.token import TokenT
from src.models.user import UserDcT


async def require_email_forgot_pwd_ctrl(
    _: Request,
    us_d: UserDcT = Depends(require_email_mdw),
) -> ResAPI:
    async with db_trx() as trx:

        await gen_token_send_email_svc(
            trx,
            us_d,
            TokenT.RECOVER_PWD,
        )

        return ResAPI.ok_201(msg="📮 email sent")


async def confirm_email_ctrl(
    _: Request,
    us_d: UserDcT = Depends(require_email_mdw),
) -> ResAPI:

    if us_d["is_verified"]:
        raise ErrAPI(msg="user already verified", status=409)
    async with db_trx() as trx:

        await gen_token_send_email_svc(
            trx,
            us_d,
            TokenT.CONF_EMAIL,
        )

        return ResAPI.ok_201(msg="📮 email sent", user=us_d)
