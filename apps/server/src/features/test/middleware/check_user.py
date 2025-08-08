from typing import Any
from fastapi import Request
from pydantic import BaseModel, Field, field_validator

from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.middleware.check_form import check_form_mdw


class UserT(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: str = Field(..., max_length=50)
    age: int

    @field_validator("age")
    def check_age(cls: Any, v: int) -> int:
        if v <= 0:
            raise ErrAPI(
                msg="Age must be an int greater than 0",
                status=422,
            )

        return v


async def check_user_mdw(
    req: Request,
) -> ResAPI | UserT:
    data = check_form_mdw(UserT, await req.body())

    return data
