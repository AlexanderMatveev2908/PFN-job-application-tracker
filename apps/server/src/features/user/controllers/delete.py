from fastapi import Depends, Request
from fastapi.responses import Response
from sqlalchemy import delete

from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.lib.cookies import gen_clear_refresh_token
from src.lib.db.idx import get_us_by_id
from src.middleware.combo.idx import (
    ComboCheckJwtCbcReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.backup_code import BackupCode
from src.models.job_application import JobApplication
from src.models.token import Token, TokenT


async def delete_account_ctrl(
    req: Request,
    result_cbc: ComboCheckJwtCbcReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            token_t=TokenT.MANAGE_ACC,
            check_jwt=True,
        )
    ),
) -> Response:

    async with db_trx() as trx:
        us = await get_us_by_id(
            trx, result_cbc["cbc_hmac_result"]["decrypted"]["user_id"]
        )

        await trx.execute(delete(Token).where(Token.user_id == us.id))

        await trx.execute(
            delete(BackupCode).where(BackupCode.user_id == us.id)
        )

        await trx.execute(
            delete(JobApplication).where(JobApplication.user_id == us.id)
        )

        await trx.delete(
            us,
        )

    return ResAPI(req, clear_cookies=[gen_clear_refresh_token()]).ok_200(
        msg="user account deleted"
    )
