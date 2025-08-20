from typing import cast
from fastapi import Depends, Request
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.auth.middleware.login import LoginForm, login_mdw
from src.features.auth.middleware.recover_pwd import (
    RecoverPwdMdwReturnT,
    recover_pwd_mdw,
)
from src.features.auth.middleware.register import RegisterFormT, register_mdw
from src.features.auth.services.login import login_svc
from src.features.auth.services.register import register_user_svc
from src.lib.cookies import gen_refresh_cookie
from src.lib.data_structure import pick
from src.lib.hashing.idx import check_pwd
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.models.token import Token
from src.models.user import User


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

    access_token, jwe_result = cast(
        TokensSessionsReturnT, await login_svc(login_data)
    )

    return ResAPI.ok_200(
        access_token=access_token,
        cookies=[gen_refresh_cookie(jwe_result["client_token"])],
    )


async def recover_pwd_ctrl(
    _: Request,
    data_recover_pwd: RecoverPwdMdwReturnT = Depends(recover_pwd_mdw),
) -> ResAPI:

    async with db_trx() as trx:
        us = cast(
            User,
            await trx.get(
                User, data_recover_pwd["check_cbc_hmac_result"]["user_d"]["id"]
            ),
        )

        if await check_pwd(
            hashed=us.password, plain=data_recover_pwd["new_password"]
        ):
            raise ErrAPI(
                msg="new password must be different from old one", status=400
            )

        await us.set_pwd(plain=data_recover_pwd["new_password"])

        access_token, refresh_result = await gen_tokens_session(
            trx=trx,
            user_id=us.id,
        )

        await trx.delete(
            await trx.get(
                Token,
                data_recover_pwd["check_cbc_hmac_result"]["token_d"]["id"],
            ),
        )

        return ResAPI.ok_200(
            msg="password updated",
            access_token=access_token,
            cookies=[gen_refresh_cookie(refresh_result["client_token"])],
        )
