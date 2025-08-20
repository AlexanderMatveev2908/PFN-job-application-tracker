from typing import cast

from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.features.auth.middleware.recover_pwd import RecoverPwdMdwReturnT
from src.lib.hashing.idx import check_pwd
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.models.token import Token
from src.models.user import User


async def change_pwd_svc(
    data_recover_pwd: RecoverPwdMdwReturnT,
) -> TokensSessionsReturnT:
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

        tokens_session = await gen_tokens_session(
            trx=trx,
            user_id=us.id,
        )

        await trx.delete(
            await trx.get(
                Token,
                data_recover_pwd["check_cbc_hmac_result"]["token_d"]["id"],
            ),
        )

        return tokens_session
