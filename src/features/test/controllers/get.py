import json
from fastapi import Request
from pydantic import BaseModel, Field, field_validator

from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.lib.data_structure import check_form


class User(BaseModel):
    first_name: str = Field(..., min_length=5)
    last_name: str = Field("Anonymous")
    age: int

    @field_validator("age")
    def check_age(cls, v) -> None:
        if v <= 0:
            raise ErrAPI(msg="invalid age", status=422)

        return v


async def get_test(req: Request) -> ResAPI:

    # form = getattr(req.state, "parsed_f", {})

    parsed = json.loads(await req.body())
    data = check_form(User, parsed)

    if not data["success"]:
        return ResAPI.err_422(msg=data["msg"], data=data["list_errs"])

    return ResAPI.ok_201(data=data["form"])
