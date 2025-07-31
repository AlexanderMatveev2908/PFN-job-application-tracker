from src.constants.data_structure import BoolParser


def parse_bool(v: str) -> bool | str:
    upper = v.upper()
    if upper in BoolParser.__members__:
        return BoolParser[upper].value
    return v
