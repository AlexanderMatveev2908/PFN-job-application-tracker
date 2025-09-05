from fastapi import Depends, Request
from fastapi.responses import Response

from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.lib.combo.TFA import check_2FA_lib
from src.lib.data_structure import dest_d
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.lib.validators.idx import TFAFormT
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBodyReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.token import TokenT


async def recover_pwd_2FA_ctrl(
    req: Request,
    combo_res: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=False,
            model=TFAFormT,
            token_t=TokenT.RECOVER_PWD,
        )
    ),
) -> Response:
    async with db_trx() as trx:
        _, backup_codes_left = dest_d(
            await check_2FA_lib(trx, combo_res, delete_tok_on_check=True),
            ["user", "backup_codes_left"],
        )

        us_id: str = combo_res["cbc_hmac_result"]["user_d"]["id"]

        cbc_hmac_token = (
            await gen_cbc_hmac(
                trx=trx,
                user_id=us_id,
                token_t=TokenT.RECOVER_PWD_2FA,
            )
        )["client_token"]

        return ResAPI(req).ok_200(
            msg="verification successful",
            backup_codes_left=backup_codes_left,
            cbc_hmac_token=cbc_hmac_token,
        )
