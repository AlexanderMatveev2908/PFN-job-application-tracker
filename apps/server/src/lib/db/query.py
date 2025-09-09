from sqlalchemy import BinaryExpression, Select
from sqlalchemy.orm.attributes import InstrumentedAttribute


def apply_query(
    stmt: Select, pair: tuple[InstrumentedAttribute[str], str]
) -> Select:
    col, val = pair
    words = [w for w in val.split() if w]

    for w in words:
        stmt = stmt.where(col.ilike(f"%{w}%"))

    return stmt


def build_conditions(
    col: InstrumentedAttribute[str], val: str
) -> list[BinaryExpression]:
    words = [w for w in val.split() if w]
    return [col.ilike(f"%{w}%") for w in words if words]
