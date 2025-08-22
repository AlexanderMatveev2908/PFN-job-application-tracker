from typing import TypedDict, cast
from fastapi import Request

from src.conf.db import db_trx
from src.lib.tokens.cbc_hmac import check_cbc_hmac
from src.lib.validators.idx import (
    PairCbcHmacPwdFormT,
)
from src.middleware.check_form import check_form_mdw
from src.models.token import CheckTokenReturnT, TokenT


class RecoverPwdMdwReturnT(TypedDict):
    check_cbc_hmac_result: CheckTokenReturnT
    new_password: str


async def recover_pwd_mdw(req: Request) -> RecoverPwdMdwReturnT:
    data = await check_form_mdw(PairCbcHmacPwdFormT, req)

    async with db_trx() as trx:

        return {
            "new_password": data.password,
            "check_cbc_hmac_result": await check_cbc_hmac(
                trx=trx,
                token_t=TokenT.RECOVER_PWD,
                token=cast(str, data.cbc_hmac_token),
            ),
        }
