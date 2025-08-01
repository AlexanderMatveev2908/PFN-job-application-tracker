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
