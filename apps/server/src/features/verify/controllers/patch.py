from fastapi import Depends, Request
from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.lib.combo.TFA import check_2FA_lib
from src.lib.cookies import gen_refresh_cookie
from src.lib.data_structure import dest_d
from src.lib.tokens.combo import gen_tokens_session
from src.lib.validators.idx import TFAFormT
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBodyReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.token import TokenT


async def confirm_new_email_2FA_ctrl(
    _: Request,
    combo_res: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=False,
            model=TFAFormT,
            token_t=TokenT.CHANGE_EMAIL_2FA,
        )
    ),
) -> ResAPI:

    async with db_trx() as trx:
        us, backup_codes_left = dest_d(
            await check_2FA_lib(trx, combo_res, delete_tok_on_check=True),
            ["user", "backup_codes_left"],
        )

        us.toggle_mails()

        tokens_session = await gen_tokens_session(trx=trx, user_id=us.id)

        return ResAPI.ok_200(
            msg="new email verified successfully",
            access_token=tokens_session["access_token"],
            backup_codes_left=backup_codes_left,
            cookies=[
                gen_refresh_cookie(
                    tokens_session["result_jwe"]["client_token"]
                )
            ],
        )
