from typing import TypedDict, cast
from fastapi import Request
from pydantic import BaseModel, Field, field_validator

from src.conf.db import db_trx
from src.lib.tokens.cbc_hmac import check_cbc_hmac
from src.lib.validators.idx import (
    check_basic_cbc_shape_lib,
    validate_password_lib,
)
from src.middleware.check_form import check_form_mdw
from src.models.token import CheckTokenReturnT, TokenT


class RecoverPwdFrom(BaseModel):
    new_password: str = Field(min_length=1, max_length=100)
    cbc_hmac_token: str | None = Field(default=None, validate_default=True)

    @field_validator("new_password")
    def _validate_password(cls, v: str) -> str:

        return validate_password_lib(v)

    @field_validator("cbc_hmac_token")
    def _check_token(cls, v: str) -> str:
        return check_basic_cbc_shape_lib(v)


class RecoverPwdMdwReturnT(TypedDict):
    check_cbc_hmac_result: CheckTokenReturnT
    new_password: str


async def recover_pwd_mdw(req: Request) -> RecoverPwdMdwReturnT:
    data = await check_form_mdw(RecoverPwdFrom, req)

    print(data)

    async with db_trx() as trx:

        return {
            "new_password": data.new_password,
            "check_cbc_hmac_result": await check_cbc_hmac(
                trx=trx,
                token_t=TokenT.RECOVER_PWD,
                token=cast(str, data.cbc_hmac_token),
                delete_expired=True,
            ),
        }
