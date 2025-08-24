from typing import cast
from fastapi import Depends, Request

from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.features.require_email.services.combo import gen_token_send_email_svc
from src.lib.db.idx import get_us_by_email, get_us_by_id
from src.lib.validators.idx import EmailFormT, PwdFormT
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBodyReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.token import TokenT
from src.models.user import User


async def change_pwd_ctrl(
    _: Request,
    result_combo: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            model=PwdFormT, token_t=TokenT.MANAGE_ACC, check_jwt=True
        )
    ),
) -> ResAPI:

    async with db_trx() as trx:
        us = await get_us_by_id(
            trx=trx, us_id=result_combo["cbc_hmac_result"]["user_d"]["id"]
        )
        new_pwd = result_combo["body"]["password"]

        if await us.check_pwd(plain=new_pwd):
            return ResAPI.err_400(
                msg="new password must be different from old one",
            )

        await cast(User, us).set_pwd(plain=new_pwd)

        return ResAPI.ok_200(msg="password updated")


async def change_email_ctrl(
    _: Request,
    combo_result: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=True, token_t=TokenT.MANAGE_ACC, model=EmailFormT
        )
    ),
) -> ResAPI:

    async with db_trx() as trx:
        if (
            combo_result["body"]["email"]
            == combo_result["cbc_hmac_result"]["user_d"]["email"]
        ):
            return ResAPI.err_400(msg="new email can not be same as old one")

        existing = await get_us_by_email(
            must_exists=False, trx=trx, email=combo_result["body"]["email"]
        )

        if existing:
            return ResAPI.err_409(msg="a user with this email already exists")

        us = cast(
            User,
            await get_us_by_id(
                trx, combo_result["cbc_hmac_result"]["user_d"]["id"]
            ),
        )
        us.tmp_email = combo_result["body"]["email"]

        await gen_token_send_email_svc(
            trx=trx,
            us_d=combo_result["cbc_hmac_result"]["user_d"],
            token_t=TokenT.CHANGE_EMAIL,
            email_to=combo_result["body"]["email"],
        )

        return ResAPI.ok_200(msg="email sent to new address")
