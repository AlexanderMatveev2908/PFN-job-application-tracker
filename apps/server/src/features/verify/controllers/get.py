from typing import cast
from fastapi import Depends, Request
from fastapi.responses import Response
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.lib.cookies import gen_refresh_cookie
from src.lib.db.idx import del_token_by_t, get_us_by_id
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.lib.tokens.combo import gen_tokens_session
from src.middleware.tokens.check_cbc_hmac import (
    check_cbc_hmac_with_us_mdw,
)
from src.models.token import (
    CheckTokenWithUsReturnT,
    TokenT,
)
from src.models.user import User


async def confirm_email_ctrl(
    req: Request,
    cbc_result: CheckTokenWithUsReturnT = Depends(
        check_cbc_hmac_with_us_mdw(token_t=TokenT.CONF_EMAIL)
    ),
) -> Response:

    async with db_trx() as trx:

        us_d = cbc_result["user_d"]

        if us_d["is_verified"]:
            raise ErrAPI(msg="user already verified", status=409)

        us = cast(User, await trx.get(User, us_d["id"]))

        us.verify_email()

        await del_token_by_t(trx=trx, token_t=TokenT.CONF_EMAIL, us_id=us.id)

        session_tokens = await gen_tokens_session(
            trx=trx,
            user_id=us.id,
        )

        return ResAPI(
            req,
            cookies=[
                gen_refresh_cookie(
                    session_tokens["result_jwe"]["client_token"]
                )
            ],
        ).ok_200(
            access_token=session_tokens["access_token"],
            msg="email verified",
        )


async def forgot_pwd_ctrl(
    req: Request,
    combo_result: CheckTokenWithUsReturnT = Depends(
        check_cbc_hmac_with_us_mdw(token_t=TokenT.RECOVER_PWD)
    ),
) -> Response:

    return ResAPI(req).ok_200(
        msg="verification successful",
        strategy_2FA=bool(
            combo_result["user_d"]["totp_secret"],
        ),
    )


async def confirm_new_email_ctrl(
    req: Request,
    result_cbc: CheckTokenWithUsReturnT = Depends(
        check_cbc_hmac_with_us_mdw(token_t=TokenT.CHANGE_EMAIL)
    ),
) -> Response:

    async with db_trx() as trx:
        us = cast(
            User, await get_us_by_id(trx=trx, us_id=result_cbc["user_d"]["id"])
        )

        await del_token_by_t(
            trx,
            result_cbc["decrypted"]["user_id"],
            TokenT.CHANGE_EMAIL,
        )

        if us.totp_secret:
            cbc_hmac_res = await gen_cbc_hmac(
                trx=trx,
                user_id=us.id,
                token_t=TokenT.CHANGE_EMAIL_2FA,
            )

            return ResAPI(req).ok_200(
                msg="email verified",
                cbc_hmac_token=cbc_hmac_res["client_token"],
            )

        us.toggle_mails()
        us.is_verified = True

        result_tokens = await gen_tokens_session(
            trx=trx,
            user_id=result_cbc["user_d"]["id"],
        )

        return ResAPI(
            req,
            cookies=[
                gen_refresh_cookie(
                    refresh_token=result_tokens["result_jwe"]["client_token"]
                )
            ],
        ).ok_200(
            msg="email updated successfully",
            access_token=result_tokens["access_token"],
        )
