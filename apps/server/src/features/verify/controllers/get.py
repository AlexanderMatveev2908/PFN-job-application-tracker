from typing import cast
from fastapi import Depends, Request
from sqlalchemy import delete
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.lib.cookies import gen_refresh_cookie
from src.lib.db.idx import get_us_by_id
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.lib.tokens.combo import gen_tokens_session
from src.middleware.check_cbc_hmac import (
    check_cbc_hmac_with_us_mdw,
)
from src.models.token import (
    CheckTokenWithUsReturnT,
    Token,
    TokenT,
)
from src.models.user import User


async def confirm_email_ctrl(
    _: Request,
    cbc_result: CheckTokenWithUsReturnT = Depends(
        check_cbc_hmac_with_us_mdw(token_t=TokenT.CONF_EMAIL)
    ),
) -> ResAPI:

    async with db_trx() as trx:

        us_d = cbc_result["user_d"]

        if us_d["is_verified"]:
            raise ErrAPI(msg="user already verified", status=409)

        us = cast(User, await trx.get(User, us_d["id"]))

        us.verify_email()
        await trx.execute(
            delete(Token).where(Token.id == cbc_result["token_d"]["id"])
        )

        return ResAPI.ok_200(
            msg="email verified",
            updated_user=us.to_d(exclude_keys=["password"]),
        )


async def forgot_pwd_ctrl(
    _: Request,
    __: CheckTokenWithUsReturnT = Depends(
        check_cbc_hmac_with_us_mdw(token_t=TokenT.RECOVER_PWD)
    ),
) -> ResAPI:

    return ResAPI.ok_200(msg="verification successful")


async def confirm_new_email_ctrl(
    _: Request,
    result_cbc: CheckTokenWithUsReturnT = Depends(
        check_cbc_hmac_with_us_mdw(token_t=TokenT.CHANGE_EMAIL)
    ),
) -> ResAPI:

    async with db_trx() as trx:
        us = cast(
            User, await get_us_by_id(trx=trx, us_id=result_cbc["user_d"]["id"])
        )

        if not us.totp_secret:

            us.toggle_mails()

            result_tokens = await gen_tokens_session(
                trx=trx,
                user_id=result_cbc["user_d"]["id"],
            )

            return ResAPI.ok_200(
                msg="email updated successfully",
                access_token=result_tokens["access_token"],
                cookies=[
                    gen_refresh_cookie(
                        refresh_token=result_tokens["result_jwe"][
                            "client_token"
                        ]
                    )
                ],
            )

        cbc_hmac_res = await gen_cbc_hmac(
            trx=trx,
            user_id=us.id,
            token_t=TokenT.CONF_EMAIL_2FA,
        )

        return ResAPI.ok_200(
            msg="email updated successfully",
            cbc_hmac_token=cbc_hmac_res["client_token"],
        )
