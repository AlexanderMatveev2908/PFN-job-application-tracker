from pydantic import BaseModel, EmailStr, Field, field_validator
from src.constants.reg import REG_CBC_HMAC, REG_PWD
from src.decorators.err import ErrAPI


class EmailForm(BaseModel):
    email: EmailStr = Field(min_length=1, max_length=254)


def check_basic_cbc_shape_lib(v: str | None) -> str:
    if not v:
        raise ErrAPI(msg="CBC_HMAC_NOT_PROVIDED", status=401)

    if not REG_CBC_HMAC.fullmatch(v):
        raise ErrAPI(msg="CBC_HMAC_INVALID_FORMAT", status=401)

    return v


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
