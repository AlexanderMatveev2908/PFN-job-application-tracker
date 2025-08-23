from fastapi import Depends, Request

from src.decorators.res import ResAPI
from src.lib.hashing.idx import check_pwd
from src.lib.validators.idx import PwdFormT
from src.middleware.combo.idx import (
    ComboCheckCbJwtCbcReturnT,
    combo_check_bd_jwt_bcb_hmac_mdw,
)
from src.models.token import TokenT


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

    return ResAPI.ok_200(**result_combo)
