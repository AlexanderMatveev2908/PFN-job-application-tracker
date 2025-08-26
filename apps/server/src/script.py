from typing import Any


print("script worked ✅")


nested = {
    "val": 7890,
    "level_a": {"level_b": {"level_c": {"level_d": {"val": 12345}}}},
}


def grab(d: dict[str, Any], key: str) -> Any | None:
    for k, v in d.items():
        if k == key:
            return v
        if isinstance(v, dict):
            found = grab(v, key)
            if found is not None:
                return found
    return None


print(grab(nested, "val"))
