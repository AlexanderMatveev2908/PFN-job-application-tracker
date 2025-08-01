import attr
from pydantic import BaseModel

from src.decorators.res import ResAPI


@attr.s(auto_attribs=True)
class User(BaseModel):
    first_name: str
    last_name: str
    age: int


async def get_test(user: User) -> ResAPI:

    # form = getattr(req.state, "parsed_f", {})

    return ResAPI.ok_200(user=user)
