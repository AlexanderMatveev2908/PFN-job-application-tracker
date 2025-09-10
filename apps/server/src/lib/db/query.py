from math import ceil
from typing import Type, TypedDict
from sqlalchemy import (
    BinaryExpression,
    Select,
    UnaryExpression,
    asc,
    desc,
    func,
    select,
)
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


def apply_query(
    stmt: Select, pair: tuple[InstrumentedAttribute[str], str]
) -> Select:
    col, val = pair
    words = [w for w in val.split() if w]

    for w in words:
        stmt = stmt.where(col.ilike(f"%{w}%"))

    return stmt


def build_cond_query(
    col: InstrumentedAttribute[str], val: str
) -> list[BinaryExpression]:
    words = [w for w in val.split() if w]
    return [col.ilike(f"%{w}%") for w in words if words]


def build_list_cond_query(
    query: dict,
    Table: Type[DeclarativeBase],
    keys: list[str],
) -> list[BinaryExpression]:
    cond: list[BinaryExpression] = []

    for k in keys:

        val: str = (query.get(k, "") or "").strip()
        cond += build_cond_query(getattr(Table, k), val)

    return cond


class ApplyPagReturnT(TypedDict):
    stmt_paginated: Select
    limit: int
    offset: int
    n_hits: int
    pages: int


async def apply_pagination(
    trx: AsyncSession,
    stmt: Select,
    query: dict,
) -> ApplyPagReturnT:

    n_hits: int = (
        await trx.execute(select(func.count()).select_from(stmt.subquery()))
    ).scalar_one()

    page = int(query["page"])
    limit = int(query["limit"])
    offset = page * limit

    pages = ceil(n_hits / limit)

    stmt_paginated = stmt.limit(limit).offset(offset)

    return {
        "stmt_paginated": stmt_paginated,
        "limit": limit,
        "offset": offset,
        "n_hits": n_hits,
        "pages": pages,
    }


def build_order_query(
    q: dict, Table: Type[DeclarativeBase], keys: list[str]
) -> list[UnaryExpression]:
    sort_clauses: list[UnaryExpression] = []

    for k in keys:
        val = q.get(k, "") or ""
        if not val:
            continue

        parsed_key_sort = k.replace("_sort", "")
        col = getattr(Table, parsed_key_sort)

        sort_clauses.append(asc(col) if val == "ASC" else desc(col))

    return sort_clauses
