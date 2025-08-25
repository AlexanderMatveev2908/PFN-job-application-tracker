from fastapi import Depends, Request
from sqlalchemy import delete, func, select
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.auth.middleware.login_totp import TotpFormT
from src.features.user.middleware.manage_account import get_access_account_mdw
from src.lib.TFA.backup import gen_backup_codes
from src.lib.db.idx import get_us_by_id
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBodyReturnT,
    ComboCheckJwtCbcReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.backup_code import BackupCode
from src.models.token import GenTokenReturnT, Token, TokenT
from src.models.user import UserDcT


async def get_access_account_ctrl(
    req: Request, us: UserDcT = Depends(get_access_account_mdw)
) -> ResAPI:

    async with db_trx() as trx:

        result_cbc: GenTokenReturnT = await gen_cbc_hmac(
            trx=trx,
            user_id=us["id"],
            token_t=(
                TokenT.MANAGE_ACC
                if not us["totp_secret"]
                else TokenT.MANAGE_ACC_2FA
            ),
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

    us_id: str = result_combo["cbc_hmac_result"]["user_d"]["id"]

    async with db_trx() as trx:

        existent_count = (
            await trx.execute(
                select(func.count())
                .select_from(BackupCode)
                .where(BackupCode.user_id == us_id)
            )
        ).scalar_one()

        if existent_count:
            raise ErrAPI(msg="user already has backup codes", status=409)

        result_codes = await gen_backup_codes(trx=trx, us_id=us_id)

    return ResAPI.ok_200(backup_codes=result_codes["backup_codes_client"])


async def get_access_manage_account_TFA_ctrl(
    req: Request,
    combo_result: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=True, model=TotpFormT, token_t=TokenT.MANAGE_ACC_2FA
        )
    ),
) -> ResAPI:

    async with db_trx() as trx:

        us = await get_us_by_id(
            trx, combo_result["cbc_hmac_result"]["user_d"]["id"]
        )

        if not us.check_totp(user_code=combo_result["body"]["totp_code"]):
            raise ErrAPI(msg="TOTP_CODE_INVALID", status=401)

        cbc_result: GenTokenReturnT = await gen_cbc_hmac(
            trx=trx,
            token_t=TokenT.MANAGE_ACC,
            user_id=us.id,
        )

        await trx.execute(
            delete(Token).where(
                (Token.token_t == TokenT.MANAGE_ACC_2FA)
                & (Token.user_id == us.id)
            )
        )

        return ResAPI.ok_200(cbc_hmac_token=cbc_result["client_token"])
