from fastapi import Depends, Request
from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.features.user.middleware.manage_account import get_access_account_mdw
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.middleware.combo.idx import (
    ComboCheckJwtCbcReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.token import GenTokenReturnT, TokenT
from src.models.user import UserDcT


async def get_access_account_ctrl(
    req: Request, us: UserDcT = Depends(get_access_account_mdw)
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


async def new_backup_codes_ctrl(
    req: Request,
    result_combo: ComboCheckJwtCbcReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            token_t=TokenT.MANAGE_ACC,
            check_jwt=True,
        )
    ),
) -> ResAPI:
    return ResAPI.ok_200(**result_combo)
