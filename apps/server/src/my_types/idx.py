from typing import Literal, TypeVar, TypedDict

from pydantic import BaseModel

from src.models.user import UserDcT

ParamWindowTime = Literal["15s", "30s", "60s", "15m", "30m", "1h", "1d"]

MAPPER_WINDOW_TIME: dict[ParamWindowTime, int] = {
    "15s": 15,
    "30s": 30,
    "60s": 60,
    "15m": 60 * 15,
    "30m": 60 * 30,
    "1h": 60**2,
    "1d": 24 * 60**2,
}

FormT = TypeVar("FormT", bound=BaseModel)


class UserDctReturnT(TypedDict):
    us_d: UserDcT
