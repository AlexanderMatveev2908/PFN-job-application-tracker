from src.lib.data_structure import parse_bool


def test_() -> None:
    res = parse_bool("true")

    assert res is True
    assert isinstance(res, bool)
