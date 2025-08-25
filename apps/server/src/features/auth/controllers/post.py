from typing import cast
from fastapi import Depends, Request
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.auth.middleware.login import LoginForm, login_mdw
from src.features.auth.middleware.register import RegisterFormT, register_mdw
from src.features.auth.services.login import login_svc
from src.features.auth.services.register import register_user_svc
from src.lib.cookies import gen_refresh_cookie
from src.lib.data_structure import parse_id, pick
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.lib.tokens.combo import gen_tokens_session
from src.lib.tokens.jwe import check_jwe_with_us
from src.lib.tokens.jwt import gen_jwt
from src.models.token import CheckTokenWithUsReturnT, TokenT


async def register_ctrl(
    _: Request, user_data: RegisterFormT = Depends(register_mdw)
) -> ResAPI:

    result = await register_user_svc(user_data)

    return ResAPI.ok_201(
        **pick(obj=cast(dict, result), keys_off=["refresh_token"]),
        cookies=[
            gen_refresh_cookie(result["refresh_token"]),
        ],
    )


async def login_ctrl(
    _: Request, login_data: LoginForm = Depends(login_mdw)
) -> ResAPI:
    async with db_trx() as trx:
        us = await login_svc(login_data=login_data, trx=trx)

        if us.totp_secret:
            cbc_hmac_result = await gen_cbc_hmac(
                token_t=TokenT.LOGIN_2FA,
                trx=trx,
                user_id=us.id,
            )
            return ResAPI.ok_200(
                cbc_hmac_token=cbc_hmac_result["client_token"],
                user_id=parse_id(us.id),
            )

        tokens_session = await gen_tokens_session(user_id=us.id, trx=trx)
        return ResAPI.ok_200(
            access_token=tokens_session["access_token"],
            cookies=[
                gen_refresh_cookie(
                    tokens_session["result_jwe"]["client_token"]
                )
            ],
        )


async def refresh_token_ctrl(req: Request) -> ResAPI:
    refresh = req.cookies.get("refresh_token")

    if not refresh:
        raise ErrAPI(msg="REFRESH_TOKEN_NOT_PROVIDED", status=401)

    async with db_trx() as trx:
        try:
            result_jwe: CheckTokenWithUsReturnT = await check_jwe_with_us(
                token=refresh, trx=trx
            )
            access_token = gen_jwt(user_id=result_jwe["user_d"]["id"])

            return ResAPI.ok_200(access_token=access_token)
        except Exception as err:
            msg = err.msg if isinstance(err, ErrAPI) else str(err)

            return ResAPI.err_401(msg=msg, clear_cookies=["refresh_token"])


async def login_totp_ctrl(req: Request) -> ResAPI:
    return ResAPI.ok_200()


async def login_backup_code_ctrl(req: Request) -> ResAPI:
    return ResAPI.ok_200()
