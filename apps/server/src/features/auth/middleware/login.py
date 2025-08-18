from fastapi import Request
from pydantic import BaseModel, EmailStr, Field, field_validator

from src.lib.validators.idx import validate_password_lib
from src.middleware.check_form import check_form_mdw


class LoginForm(BaseModel):
    email: EmailStr = Field(min_length=1, max_length=254)
    password: str = Field(min_length=1, max_length=100)

    @field_validator("password")
    def _validate_password(cls, v: str) -> str:

        return validate_password_lib(v)


async def login_mdw(req: Request) -> LoginForm:
    data = await check_form_mdw(LoginForm, req)

    return data
