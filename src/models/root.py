from datetime import datetime
from typing import Any, Optional
import uuid
from sqlalchemy import TIMESTAMP, func, inspect
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.attributes import NO_VALUE  # type: ignore # noqa: E501


Base = declarative_base()
Base.metadata.schema = "public"


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

    def to_d(self, join: bool = False, depth: int = 0) -> dict[str, Any]:
        mapper = inspect(self.__class__)
        state = inspect(self)
        out: dict[str, Any] = {}

        for col in mapper.columns:
            val = getattr(self, col.key)
            if isinstance(val, uuid.UUID):
                val = str(val)
            elif isinstance(val, datetime):
                val = val.isoformat()
            out[col.key] = val

        if join and depth > 0:
            for rel in mapper.relationships:
                attr = state.attrs[rel.key]

                loaded = attr.loaded_value is not NO_VALUE
                if not loaded:
                    continue

                v = attr.value
                if v is None:
                    out[rel.key] = None
                elif rel.uselist:
                    out[rel.key] = [
                        item.to_d(join=True, depth=depth - 1) for item in v
                    ]
                else:
                    out[rel.key] = v.to_d(join=True, depth=depth - 1)
        return out
