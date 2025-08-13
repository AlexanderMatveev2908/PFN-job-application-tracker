from typing import Self
from fastapi import Request
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    model_validator,
)

from src.constants.reg import REG_NAME, REG_PWD
from src.decorators.err import ErrAPI
from src.middleware.check_form import check_form_mdw


class RegisterForm(BaseModel):
    first_name: str = Field(min_length=1, max_length=50, pattern=REG_NAME)
    last_name: str = Field(min_length=1, max_length=50, pattern=REG_NAME)

    email: EmailStr = Field(min_length=1, max_length=100)

    password: str = Field(min_length=1, max_length=100, pattern=REG_PWD)
    confirm_password: str = Field(min_length=1, max_length=100)

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ErrAPI(msg="Passwords do not match", status=422)
        return self


async def register_mdw(req: Request) -> None:
    data = check_form_mdw(RegisterForm, await req.body())

    return data
