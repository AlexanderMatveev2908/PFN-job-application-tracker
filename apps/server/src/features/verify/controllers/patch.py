from typing import cast
from fastapi import Depends, Request
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.auth.middleware.login_totp import TotpFormT
from src.lib.cookies import gen_refresh_cookie
from src.lib.db.idx import get_us_by_id
from src.lib.etc import grab
from src.lib.tokens.combo import gen_tokens_session
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBodyReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.token import TokenT
from src.models.user import User


async def confirm_new_email_2FA_top_ctrl(
    _: Request,
    combo_result: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=False, model=TotpFormT, token_t=TokenT.CHANGE_EMAIL_2FA
        )
    ),
) -> ResAPI:

    async with db_trx() as trx:

        us = cast(
            User,
            await get_us_by_id(
                trx=trx, us_id=grab(combo_result, "id", parent="user_d")
            ),
        )

        if not us.check_totp(user_code=combo_result["body"]["totp_code"]):
            raise ErrAPI(msg="totp_code_invalid", status=401)

        us.toggle_mails()

        tokens_session = await gen_tokens_session(trx=trx, user_id=us.id)

        return ResAPI.ok_200(
            msg="new email verified successfully",
            access_token=tokens_session["access_token"],
            cookies=[
                gen_refresh_cookie(
                    tokens_session["result_jwe"]["client_token"]
                )
            ],
        )
