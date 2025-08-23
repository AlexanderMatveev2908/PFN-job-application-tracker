from typing import cast
from fastapi import Depends, Request

from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.lib.hashing.idx import check_pwd
from src.lib.validators.idx import PwdFormT
from src.middleware.combo.idx import (
    ComboCheckCbJwtCbcReturnT,
    combo_check_bd_jwt_bcb_hmac_mdw,
)
from src.models.token import TokenT
from src.models.user import User


async def change_pwd_ctrl(
    _: Request,
    result_combo: ComboCheckCbJwtCbcReturnT = Depends(
        combo_check_bd_jwt_bcb_hmac_mdw(
            model=PwdFormT, token_t=TokenT.MANAGE_ACC, check_jwt=True
        )
    ),
) -> ResAPI:

    new_pwd = result_combo["body"]["password"]

    if await check_pwd(
        hashed=result_combo["cbc_hmac_result"]["user_d"]["password"],
        plain=new_pwd,
    ):
        return ResAPI.err_400(
            msg="new password must be different from old one",
        )

    async with db_trx() as trx:
        us = await trx.get(
            User, result_combo["cbc_hmac_result"]["user_d"]["id"]
        )

        await cast(User, us).set_pwd(plain=new_pwd)

        return ResAPI.ok_200()
