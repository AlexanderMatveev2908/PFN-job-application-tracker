import datetime
from enum import Enum
import json
import re
from typing import Any, Mapping, Optional, Sequence
import uuid

from pydantic import BaseModel
from sqlalchemy import inspect
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


def is_list_ok(arg: Optional[list[Any]]) -> bool:
    if arg is None:
        return False

    return bool(arg) and any(el is not None for el in (arg))


def is_id_ok(v: str) -> bool:
    try:
        return uuid.UUID(v).version == 4
    except Exception:
        return False


def t_str(v: str | None, reg: re.Pattern[str]) -> bool:
    if not v:
        return False

    return bool(reg.match(v))


def serialize(obj: Any, depth: int, max_depth: int = 0) -> Any:
    if depth > max_depth:
        return f"max_depth => {type(obj).__name__}"

    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj

    try:
        state = inspect(obj)
        if hasattr(state, "mapper"):
            mapper = state.mapper
            d: dict[str, Any] = {}

            for col in mapper.columns:
                v = getattr(obj, col.key)

                if isinstance(v, uuid.UUID):
                    v = str(v)
                elif isinstance(v, (datetime.datetime, datetime.date)):
                    v = v.isoformat()

                d[col.key] = v
            return serialize(d, depth + 1, max_depth)
    except Exception:
        pass

    if isinstance(obj, BaseModel):
        return serialize(obj.model_dump(), depth + 1, max_depth)

    if isinstance(obj, (bytes, bytearray)):
        try:
            return "some long string 👻"
            # return obj.decode("utf-8")
        except Exception:
            return list(obj)

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()

    if isinstance(obj, Enum):
        return obj.value

    if isinstance(obj, (set)):
        return [serialize(v, depth + 1, max_depth) for v in obj]

    if isinstance(obj, Mapping):
        return {
            str(k): serialize(v, depth + 1, max_depth) for k, v in obj.items()
        }

    if isinstance(obj, Sequence) and not isinstance(
        obj, (str, bytes, bytearray)
    ):
        return [serialize(v, depth + 1, max_depth) for v in obj]

    if hasattr(obj, "__dict__"):
        return serialize(vars(obj), depth + 1, max_depth)

    return obj


def h_to_b(txt_hex: str) -> bytes:
    return bytes.fromhex(txt_hex)


def b_to_h(b: bytes) -> str:
    return b.hex()


def d_to_b(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )


def b_to_d(b: bytes) -> dict:
    return json.loads(
        b.decode("utf-8"),
    )
