from typing import Self, TypedDict
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)
from src.constants.reg import (
    REG_BACKUP_CODE,
    REG_CBC_HMAC,
    REG_PWD,
    REG_TOTP_CODE,
)
from src.decorators.err import ErrAPI
from src.lib.db.idx import get_us_by_id
from src.lib.etc import grab
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class EmailFormT(BaseModel):
    email: EmailStr = Field(min_length=1, max_length=254)


def validate_password_lib(v: str) -> str:

    if not REG_PWD.match(v):
        raise ErrAPI(
            msg="Password must have at least 1 lowercase, 1 uppercase, "
            "1 number, 1 symbol, and be 8+ chars long",
            status=422,
        )
    return v


class PwdFormT(BaseModel):
    password: str = Field(
        min_length=1,
        max_length=100,
    )

    @field_validator("password")
    def _validate_password(cls, v: str) -> str:

        return validate_password_lib(v)


def check_basic_cbc_shape_lib(v: str | None) -> str:
    if not v:
        raise ErrAPI(msg="cbc_hmac_not_provided", status=401)

    if not REG_CBC_HMAC.fullmatch(v):
        raise ErrAPI(msg="cbc_hmac_invalid_format", status=401)

    return v


class Check2FAFormT(BaseModel):
    totp_code: str | None = Field(default=None, pattern=REG_TOTP_CODE)
    backup_code: str | None = Field(default=None, pattern=REG_BACKUP_CODE)

    @model_validator(mode="after")
    def check_one_or_throw(self) -> Self:
        if not self.totp_code and not self.backup_code:
            raise ErrAPI(
                msg="neither totp_code nor backup_code provided",
                status=401,
            )
        return self


class Check2FALibReturnT(TypedDict):
    backup_codes_left: int | None
    user: User


async def check_2FA_lib(
    trx: AsyncSession, res_combo: ComboCheckJwtCbcBodyReturnT
) -> Check2FALibReturnT:

    us = await get_us_by_id(trx, grab(res_combo, "user_id"))
    backup_codes_left: int | None = None

    if totp_code := grab(res_combo, "totp_code"):
        us.check_totp(totp_code)
    elif backup_code := (grab(res_combo, "backup_code")):
        backup_codes_left = (await us.check_backup_code(trx, backup_code))[
            "backup_codes_left"
        ]

    return {"user": us, "backup_codes_left": backup_codes_left}
