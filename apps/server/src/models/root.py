from typing import Any, Optional
import uuid
from sqlalchemy import BigInteger, MetaData, text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from sqlalchemy.dialects.postgresql import UUID

from src.lib.serialize_data import serialize


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

        return serialize(
            self, joins=joins, max_depth=max_depth, exclude_keys=exclude_keys
        )
