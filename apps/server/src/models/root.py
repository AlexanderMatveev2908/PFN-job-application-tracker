from datetime import date, datetime
from typing import Any, Optional, cast
import uuid
from sqlalchemy import TIMESTAMP, MetaData, func, inspect
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Mapper,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.state import InstanceState


class Base(DeclarativeBase):
    metadata = MetaData(schema="public")


class RootTable(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    def to_d(self, joins: bool = False, max_depth: int = 0) -> dict[str, Any]:
        state = cast(InstanceState[Any], inspect(self))
        mapper: Mapper[Any] = state.mapper

        out: dict[str, Any] = {}

        for col in mapper.columns:
            val = getattr(self, col.key)
            if isinstance(val, uuid.UUID):
                val = str(val)
            elif isinstance(val, (datetime, date)):
                val = val.isoformat()
            out[col.key] = val

        if joins and max_depth > 0:
            for rel in mapper.relationships:
                attr = state.attrs[rel.key]

                if rel.key in state.unloaded:
                    continue

                v = attr.value
                if v is None:
                    out[rel.key] = None
                elif rel.uselist:
                    out[rel.key] = [
                        item.to_d(joins=True, max_depth=max_depth - 1)
                        for item in v
                    ]
                else:
                    out[rel.key] = v.to_d(joins=True, max_depth=max_depth - 1)
        return out
