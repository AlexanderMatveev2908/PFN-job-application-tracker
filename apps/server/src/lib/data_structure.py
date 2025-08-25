from enum import Enum
import json
import re
from typing import Any, Optional
import uuid
from src.decorators.err import ErrAPI


class BoolParser(Enum):
    TRUE = True
    FALSE = False


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


def h_to_b(txt_hex: str) -> bytes:
    return bytes.fromhex(txt_hex)


def b_to_h(b: bytes) -> str:
    return b.hex()


def d_to_b(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )


def b_to_d(
    b: bytes, err_msg: str = "wrong data format", err_status: int = 422
) -> dict:
    try:
        return json.loads(
            b.decode("utf-8"),
        )

    except Exception:
        raise ErrAPI(msg=err_msg, status=err_status)


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


def pick(
    obj: dict,
    keys_in: Optional[list[str]] = None,
    keys_off: Optional[list[str]] = None,
) -> dict:
    return {
        k: obj[k]
        for k in obj.keys()
        if (keys_in is None or k in keys_in)
        and (keys_off is None or k not in keys_off)
    }


def dest_d(d: dict, keys: list[str]) -> tuple:
    return tuple(d[k] for k in keys if k in d)
