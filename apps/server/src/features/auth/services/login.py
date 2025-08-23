from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.features.auth.middleware.login import LoginForm
from src.lib.db.idx import get_us_by_email
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session


async def login_svc(login_data: LoginForm) -> TokensSessionsReturnT:
    async with db_trx() as trx:
        us = await get_us_by_email(trx, email=login_data.email)

        if not us:
            raise ErrAPI(msg="user not found", status=404)

        res_argon = await us.check_pwd(login_data.password)

        if not res_argon:
            raise ErrAPI(msg="invalid credentials", status=401)

        return await gen_tokens_session(user_id=us.id, trx=trx)
