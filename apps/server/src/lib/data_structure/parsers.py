from enum import Enum
from typing import Any
import uuid

from src.decorators.err import ErrAPI
from src.middleware.parsers.form_data_parser.types import ParsedValue


def assign_nested_parser(d: dict, key: str, val: ParsedValue) -> None:
    parts = key.replace("]", "").split("[")

    curr = d
    # ? not parts[-1] means it is a list like mangos[]
    # ? and not a typical nested dict fruits[bananas]
    stop = -2 if not parts[-1] else -1

    for p in parts[:stop]:
        curr = curr.setdefault(p, {})
    last = parts[-1]

    if not last:
        arr = curr.setdefault(parts[-2], [])
        if isinstance(arr, list):
            arr.append(val)
        else:
            curr[parts[-2]] = [arr, val]
    elif last in curr:
        existing = curr[last]
        if isinstance(existing, list):
            existing.append(val)
        else:
            curr[last] = [existing, val]
    else:
        curr[last] = val


class BoolParser(Enum):
    TRUE = True
    FALSE = False


def parse_bool(v: Any) -> bool | str:
    if isinstance(v, str):
        upper = v.upper()
        if upper in BoolParser.__members__:
            return BoolParser[upper].value
    return v


def parse_id(id: str | uuid.UUID) -> str:
    if isinstance(id, str):
        return id
    elif isinstance(id, uuid.UUID):
        return str(id)
    else:
        raise ErrAPI(msg="invalid id passed as arg", status=500)


def parse_enum(v: Enum | str) -> str:
    if isinstance(v, str):
        return v
    if isinstance(v, Enum) or issubclass(v, Enum):
        return v.value
    else:
        raise ErrAPI(msg="invalid v, neither enum or str", status=500)
