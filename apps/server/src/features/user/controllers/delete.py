from fastapi import Depends, Request
from sqlalchemy import text

from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.lib.db.idx import get_us_by_id
from src.middleware.combo.idx import (
    ComboCheckJwtCbcReturnT,
    combo_check_bd_jwt_bcb_hmac_mdw,
)
from src.models.token import TokenT


async def delete_account_ctrl(
    req: Request,
    result_cbc: ComboCheckJwtCbcReturnT = Depends(
        combo_check_bd_jwt_bcb_hmac_mdw(
            token_t=TokenT.MANAGE_ACC,
            check_jwt=True,
        )
    ),
) -> ResAPI:

    async with db_trx() as trx:
        us = await get_us_by_id(
            trx, result_cbc["cbc_hmac_result"]["user_d"]["id"]
        )

        await trx.execute(
            text("DELETE FROM tokens AS tk " "WHERE tk.user_id = :user_id"),
            {"user_id": us.id},
        )

        await trx.delete(
            us,
        )

    return ResAPI.ok_200(msg="user account deleted")
