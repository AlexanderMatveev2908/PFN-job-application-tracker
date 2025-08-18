from datetime import date, datetime
from typing import Any, Optional, cast
import uuid
from sqlalchemy import BigInteger, MetaData, inspect, text
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

    created_at: Mapped[int] = mapped_column(
        BigInteger,
        server_default=text("(extract(epoch from now()) * 1000)::bigint"),
        nullable=False,
    )

    updated_at: Mapped[int] = mapped_column(
        BigInteger,
        server_default=text("(extract(epoch from now()) * 1000)::bigint"),
        server_onupdate=text("(extract(epoch from now()) * 1000)::bigint"),
        nullable=False,
    )

    deleted_at: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
    )

    def to_d(
        self,
        *,
        joins: bool = False,
        max_depth: int = 0,
        exclude_keys: list[str] = [],
    ) -> dict[str, Any]:
        state = cast(InstanceState[Any], inspect(self))
        mapper: Mapper[Any] = state.mapper
        sd = state.dict

        def _ser(v: Any) -> Any:
            if isinstance(v, uuid.UUID):
                return str(v)
            if isinstance(v, (datetime, date)):
                return v.isoformat()
            return v

        out: dict[str, Any] = {}

        for col in mapper.columns:
            k = col.key
            if k in exclude_keys:
                continue
            if k in sd:
                out[k] = _ser(sd[k])

        if joins and max_depth > 0:
            for rel in mapper.relationships:
                k = rel.key
                if k in exclude_keys:
                    continue
                if k not in sd:
                    continue

                v = sd[k]
                if v is None:
                    out[k] = None
                elif rel.uselist:
                    out[k] = [
                        item.to_d(
                            joins=True,
                            max_depth=max_depth - 1,
                            exclude_keys=exclude_keys,
                        )
                        for item in v
                    ]
                else:
                    out[k] = v.to_d(
                        joins=True,
                        max_depth=max_depth - 1,
                        exclude_keys=exclude_keys,
                    )

        return out
