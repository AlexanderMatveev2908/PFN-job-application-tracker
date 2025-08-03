import uuid
from sqlalchemy import TIMESTAMP, Column, func
from sqlmodel import SQLModel
from sqlalchemy.orm import declared_attr
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class RootMixin:
    @declared_attr
    def id(cls):
        return Column(
            PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
        )

    @declared_attr
    def created_at(cls):
        return Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
        )

    @declared_attr
    def updated_at(cls):
        return Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        )

    @declared_attr
    def deleted_at(cls):
        return Column(TIMESTAMP(timezone=True), nullable=True)


class RootTable(SQLModel, RootMixin):
    __abstract__ = True
    __table_args__ = {"schema": "public"}

    def to_d(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}  # type: ignore # noqa: E501


# from datetime import datetime
# import uuid
# from sqlalchemy import TIMESTAMP, func
# from sqlalchemy.orm import declarative_base, Mapped, mapped_column
# from sqlalchemy.dialects.postgresql import UUID

# Base = declarative_base()
# Base.metadata.schema = "public"

# class RootTable(Base):
#     __abstract__ = True

#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         TIMESTAMP(timezone=True),
#         server_default=func.now(),
#         onupdate=func.now(),
#         nullable=False,
#     )
#     deleted_at: Mapped[datetime] = mapped_column(
#         TIMESTAMP(timezone=True), nullable=True
#     )

#     def to_d(self) -> dict:
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns} # noqa: E501
