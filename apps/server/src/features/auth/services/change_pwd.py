from typing import cast

from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT
from src.models.token import Token
from src.models.user import User


async def change_pwd_svc(
    result_combo: ComboCheckJwtCbcBodyReturnT,
) -> TokensSessionsReturnT:
    async with db_trx() as trx:
        us = cast(
            User,
            await trx.get(
                User, result_combo["cbc_hmac_result"]["user_d"]["id"]
            ),
        )

        if await us.check_pwd(plain=result_combo["body"]["password"]):
            raise ErrAPI(
                msg="new password must be different from old one", status=400
            )

        await us.set_pwd(plain=result_combo["body"]["password"])

        tokens_session = await gen_tokens_session(
            trx=trx,
            user_id=us.id,
        )

        await trx.delete(
            await trx.get(
                Token,
                result_combo["cbc_hmac_result"]["token_d"]["id"],
            ),
        )

        return tokens_session
