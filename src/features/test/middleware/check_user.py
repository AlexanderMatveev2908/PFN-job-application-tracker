import json
from fastapi import Request
from pydantic import BaseModel, Field, field_validator

from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.lib.form_check import CheckFormErr, check_form


class User(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field("Unknown")
    age: int

    @field_validator("age")
    def check_age(cls, v) -> int:
        if v <= 0:
            raise ErrAPI(
                msg="Age must be an int greater than 0",
                status=422,
            )

        return v


async def check_user(
    req: Request,
) -> ResAPI | User:
    parsed = json.loads(await req.body())
    data = check_form(User, parsed)

    if isinstance(data, CheckFormErr):
        raise ErrAPI(
            msg=data.msg,
            status=422,
            list_errs=data.list_errs,
        )

    return data.form
