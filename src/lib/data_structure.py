from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError
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


def check_form(model: Type[FormT], data: dict) -> dict:
    try:
        instance = model(**data)
        return {"success": True, "form": instance}
    except ValidationError as err:
        arg_errs = err.errors()
        return {
            "success": False,
            "msg": f'📌 {arg_errs[0]["loc"][0]} => 💣 {arg_errs[0]["msg"]}',
            "list_errs": arg_errs,
        }
