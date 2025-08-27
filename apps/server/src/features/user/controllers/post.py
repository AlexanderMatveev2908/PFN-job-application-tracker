from fastapi import Depends, Request
from sqlalchemy import func, select
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.auth.middleware.login_backup_code import BackupCodeFormT
from src.features.auth.middleware.login_totp import TotpFormT
from src.features.user.middleware.manage_account import get_access_account_mdw
from src.lib.TFA.backup import gen_backup_codes
from src.lib.db.idx import del_token_by_t, get_us_by_id
from src.lib.etc import grab
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.lib.validators.idx import Check2FAFormT
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBodyReturnT,
    ComboCheckJwtCbcReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.backup_code import BackupCode
from src.models.token import GenTokenReturnT, TokenT
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

    us_id: str = grab(result_combo, "user_id")

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


async def get_access_manage_account_2FA_ctrl(
    req: Request,
    res_combo: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=True, model=Check2FAFormT, token_t=TokenT.MANAGE_ACC_2FA
        )
    ),
) -> ResAPI:

    return ResAPI.ok_200()


async def get_access_manage_account_TFA_totp_ctrl(
    req: Request,
    combo_result: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=True, model=TotpFormT, token_t=TokenT.MANAGE_ACC_2FA
        )
    ),
) -> ResAPI:

    async with db_trx() as trx:

        us = await get_us_by_id(trx, grab(combo_result, "user_id"))

        us.check_totp(user_code=combo_result["body"]["totp_code"])

        cbc_result: GenTokenReturnT = await gen_cbc_hmac(
            trx=trx,
            token_t=TokenT.MANAGE_ACC,
            user_id=us.id,
        )

        await del_token_by_t(trx, us.id, TokenT.MANAGE_ACC_2FA)

        return ResAPI.ok_200(cbc_hmac_token=cbc_result["client_token"])


async def get_access_manage_account_backup_code_ctrl(
    req: Request,
    combo_result: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=True,
            model=BackupCodeFormT,
            token_t=TokenT.MANAGE_ACC_2FA,
        )
    ),
) -> ResAPI:

    async with db_trx() as trx:

        us = await get_us_by_id(trx, grab(combo_result, "user_id"))

        res_backup_check = await us.check_backup_code(
            trx, backup_code=grab(combo_result, "backup_code")
        )

        await del_token_by_t(trx, us.id, TokenT.MANAGE_ACC_2FA)

        cbc_result: GenTokenReturnT = await gen_cbc_hmac(
            trx=trx,
            token_t=TokenT.MANAGE_ACC,
            user_id=us.id,
        )

        return ResAPI.ok_200(
            cbc_hmac_token=cbc_result["client_token"],
            backup_codes_left=res_backup_check["backup_codes_left"],
        )
