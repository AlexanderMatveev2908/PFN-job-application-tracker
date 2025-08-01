import dataclasses
from typing import Generic, Type, TypeVar
from pydantic import BaseModel, ValidationError
from pydantic_core import ErrorDetails

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
