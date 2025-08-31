from fastapi import Request, Response

from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.lib.tokens.jwe import check_jwe_with_us
from src.lib.tokens.jwt import gen_jwt
from src.models.token import CheckTokenWithUsReturnT


async def refresh_token_ctrl(req: Request) -> Response:
    refresh = req.cookies.get("refresh_token")

    if not refresh:
        raise ErrAPI(msg="jwe_not_provided", status=401)

    async with db_trx() as trx:
        try:
            result_jwe: CheckTokenWithUsReturnT = await check_jwe_with_us(
                token=refresh, trx=trx
            )
            access_token = gen_jwt(user_id=result_jwe["user_d"]["id"])

            return ResAPI(req).ok_200(access_token=access_token)
        except Exception as err:
            msg = err.msg if isinstance(err, ErrAPI) else str(err)

            return ResAPI(req, clear_cookies=["refresh_token"]).err_401(
                msg=msg,
            )
