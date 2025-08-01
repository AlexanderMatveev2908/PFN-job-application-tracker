import dataclasses
from typing import Generic, Type, TypeVar
from pydantic import BaseModel, ValidationError
from pydantic_core import ErrorDetails
from src.constants.data_structure import BoolParser


def parse_bool(v: str) -> bool | str:
    upper = v.upper()
    if upper in BoolParser.__members__:
        return BoolParser[upper].value
    return v


def is_obj_ok(obj: object | None) -> bool:

    parsed = vars(obj) if hasattr(obj, "__dict__") else obj

    if not isinstance(parsed, dict):
        return False

    return bool(len(parsed.keys())) and any(
        v is not None for v in parsed.values()
    )


FormT = TypeVar("FormT", bound=BaseModel)


@dataclasses.dataclass
class CheckForm:
    success: bool


@dataclasses.dataclass
class CheckFormOk(CheckForm, Generic[FormT]):
    form: FormT


@dataclasses.dataclass
class CheckFormErr(CheckForm):
    msg: str
    list_errs: list[ErrorDetails]


def check_form(model: Type[FormT], data: dict) -> CheckFormOk | CheckFormErr:
    try:
        instance = model(**data)
        return CheckFormOk(success=True, form=instance)
    except ValidationError as err:
        arg_errs = err.errors()
        return CheckFormErr(
            success=False,
            msg=f'📌 {arg_errs[0]["loc"][0]} => 💣 {arg_errs[0]["msg"]}',
            list_errs=arg_errs,
        )
