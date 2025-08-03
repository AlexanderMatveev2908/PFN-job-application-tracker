from typing import TYPE_CHECKING, Optional
import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlmodel import Field, Relationship
from src.models.root import RootTable
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

if TYPE_CHECKING:
    from .user import User


class Car(RootTable, table=True):
    __tablename__ = "cars"  # type: ignore

    name: str = Field(sa_column=Column(String(50), nullable=False))

    user_id: uuid.UUID = Field(
        Column(
            PG_UUID(as_uuid=True),
            ForeignKey("users.id", name="fk_car_user_id"),
            nullable=False,
        )
    )

    user: Optional["User"] = Relationship(back_populates="cars")


# from typing import TYPE_CHECKING
# import uuid
# from sqlalchemy import UUID, ForeignKey, String
# from src.models.root import RootTable
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# if TYPE_CHECKING:
#     from .user import User


# class Car(RootTable):
#     __tablename__ = "cars"

#     name: Mapped[str] = mapped_column(String(50), nullable=False)

#     user_id: Mapped[uuid.UUID] = mapped_column(
#         UUID,
#         ForeignKey("users.id", name="fk_car_user_id"),
#         nullable=False,
#     )
#     user: Mapped["User"] = relationship(back_populates="cars")
