from typing import cast
from fastapi import Depends, Request
from fastapi.responses import Response
from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.features.auth.middleware.login import LoginForm, login_mdw
from src.features.auth.middleware.register import RegisterFormT, register_mdw
from src.features.auth.services.login import login_svc
from src.features.auth.services.login_2FA import login_2FA_svc
from src.features.auth.services.register import (
    RegisterSvcReturnT,
    register_user_svc,
)
from src.lib.cookies import gen_refresh_cookie
from src.lib.db.idx import del_token_by_t
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.lib.tokens.combo import gen_tokens_session
from src.lib.validators.idx import TFAFormT
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBodyReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.middleware.tokens.check_jwt import check_jwt_search_us_mdw
from src.models.token import TokenT
from src.models.user import User, UserDcT


async def register_ctrl(
    req: Request, user_data: RegisterFormT = Depends(register_mdw)
) -> Response:

    result: RegisterSvcReturnT = await register_user_svc(user_data)

    return ResAPI(
        req,
        cookies=[
            gen_refresh_cookie(result["refresh_token"]),
        ],
    ).ok_201(
        access_token=result["access_token"],
    )


async def login_ctrl(
    req: Request, login_data: LoginForm = Depends(login_mdw)
) -> Response:
    async with db_trx() as trx:
        us = await login_svc(login_data=login_data, trx=trx)

        if us.totp_secret:
            cbc_hmac_result = await gen_cbc_hmac(
                token_t=TokenT.LOGIN_2FA,
                trx=trx,
                user_id=us.id,
            )
            return ResAPI(req).ok_200(
                cbc_hmac_token=cbc_hmac_result["client_token"],
            )

        tokens_session = await gen_tokens_session(user_id=us.id, trx=trx)
        return ResAPI(
            req,
            cookies=[
                gen_refresh_cookie(
                    tokens_session["result_jwe"]["client_token"]
                )
            ],
        ).ok_200(
            access_token=tokens_session["access_token"],
        )


async def login_2FA_ctrl(
    req: Request,
    result_combo: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=False, model=TFAFormT, token_t=TokenT.LOGIN_2FA
        )
    ),
) -> Response:

    res_check = await login_2FA_svc(result_combo)

    return ResAPI(
        req,
        cookies=[gen_refresh_cookie(res_check["result_jwe"]["client_token"])],
    ).ok_200(
        access_token=res_check["access_token"],
        backup_codes_left=res_check["backup_codes_left"],
    )


async def logout_ctrl(
    req: Request,
    us: User | UserDcT | None = Depends(
        check_jwt_search_us_mdw(optional=True)
    ),
) -> Response:

    feedback = "almost successful"
    async with db_trx() as trx:
        if us:
            await del_token_by_t(
                trx=trx, us_id=cast(UserDcT, us)["id"], token_t=TokenT.REFRESH
            )
            feedback = "successful"

    return ResAPI(req, clear_cookies=["refresh_token"]).ok_200(
        msg=f"logout {feedback}"
    )
