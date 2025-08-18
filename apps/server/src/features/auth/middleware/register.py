from typing import Self, TypedDict, cast
from fastapi import Request
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from src.constants.reg import REG_NAME
from src.decorators.err import ErrAPI
from src.lib.validators.idx import validate_password_lib
from src.middleware.check_form import check_form_mdw


class RegisterForm(BaseModel):
    first_name: str = Field(
        min_length=1, max_length=50, pattern=REG_NAME.pattern
    )
    last_name: str = Field(
        min_length=1, max_length=50, pattern=REG_NAME.pattern
    )

    email: EmailStr = Field(min_length=1, max_length=254)

    password: str = Field(min_length=1, max_length=100)
    confirm_password: str = Field(min_length=1, max_length=100)

    terms: bool = Field(
        ...,
    )

    @field_validator("password")
    def _validate_password(cls, v: str) -> str:

        return validate_password_lib(v)

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ErrAPI(msg="Passwords do not match", status=422)
        return self

    @model_validator(mode="after")
    def check_email(self) -> Self:
        if self.email == self.password:
            raise ErrAPI(
                msg="password can not be the same as the email", status=400
            )
        return self

    @field_validator("terms")
    def check_terms(cls, v: bool) -> bool:
        if v is not True:
            raise ErrAPI(msg="user must accept terms", status=422)
        return v


class RegisterFormT(TypedDict):
    first_name: str
    last_name: str
    email: str
    password: str
    terms: bool


async def register_mdw(req: Request) -> RegisterFormT:
    data = await check_form_mdw(RegisterForm, req)

    return cast(RegisterFormT, data.model_dump(exclude={"confirm_password"}))
