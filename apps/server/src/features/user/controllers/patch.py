from fastapi import Depends, Request

from src.decorators.res import ResAPI
from src.lib.validators.idx import PwdFormT
from src.middleware.combo.idx import (
    ComboCheckCbJwtCbcReturnT,
    combo_check_bd_jwt_bcb_hmac_mdw,
)
from src.models.token import TokenT


async def change_pwd_ctrl(
    _: Request,
    result_action_mdw: ComboCheckCbJwtCbcReturnT = Depends(
        combo_check_bd_jwt_bcb_hmac_mdw(
            model=PwdFormT, token_t=TokenT.MANAGE_ACC, check_jwt=True
        )
    ),
) -> ResAPI:
    return ResAPI.ok_200(**result_action_mdw)
