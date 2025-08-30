from fastapi import Depends, Request
from fastapi.responses import Response
from sqlalchemy import func, select
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.user.middleware.manage_account import get_access_account_mdw
from src.lib.TFA.backup import gen_backup_codes
from src.lib.combo.TFA import check_2FA_lib
from src.lib.data_structure import dest_d
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.lib.validators.idx import TFAFormT
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
) -> Response:

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

        return ResAPI(req).ok_200(
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
) -> Response:

    us_id: str = result_combo["cbc_hmac_result"]["decrypted"]["user_id"]

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

    return ResAPI(req).ok_200(backup_codes=result_codes["backup_codes_client"])


async def get_access_manage_account_2FA_ctrl(
    req: Request,
    res_combo: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=True, model=TFAFormT, token_t=TokenT.MANAGE_ACC_2FA
        )
    ),
) -> Response:

    async with db_trx() as trx:
        us, backup_codes_left = dest_d(
            d=await check_2FA_lib(trx, res_combo, delete_tok_on_check=True),
            keys=["user", "backup_codes_left"],
        )

        cbc_result: GenTokenReturnT = await gen_cbc_hmac(
            trx=trx,
            token_t=TokenT.MANAGE_ACC,
            user_id=us.id,
        )

        return ResAPI(req).ok_200(
            cbc_hmac_token=cbc_result["client_token"],
            backup_codes_left=backup_codes_left,
        )
