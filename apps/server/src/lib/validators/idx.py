from typing import Self
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


class TFAFormT(BaseModel):
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
