from fastapi import Depends, Request
from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.features.user.middleware.manage_account import manage_account_mdw
from src.lib.TFA.idx import GenTotpSecretReturnT, gen_totp_secret
from src.lib.algs.fernet import gen_fernet
from src.lib.db.idx import get_us_by_id
from src.lib.qrcode.idx import gen_qrcode
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBodyReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.token import GenTokenReturnT, TokenT
from src.models.user import UserDcT


async def get_access_account_ctrl(
    req: Request, us: UserDcT = Depends(manage_account_mdw)
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


async def TFA_ctrl(
    _: Request,
    result_combo: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=True, token_t=TokenT.MANAGE_ACC
        )
    ),
) -> ResAPI:

    async with db_trx() as trx:
        us = await get_us_by_id(
            trx=trx, us_id=result_combo["cbc_hmac_result"]["user_d"]["id"]
        )

        result_secret: GenTotpSecretReturnT = gen_totp_secret(
            user_email=us.email
        )

        us.totp_secret = gen_fernet(txt=result_secret["secret"])

        qrcode: str = gen_qrcode(uri=result_secret["uri"])

        return ResAPI.ok_200(
            totp_secret=result_secret["secret"], totp_secret_qrcode=qrcode
        )
