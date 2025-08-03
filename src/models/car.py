from typing import TYPE_CHECKING
import uuid
from sqlalchemy import UUID, ForeignKey, String
from src.models.root import RootTable
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User


class Car(RootTable):
    __tablename__ = "cars"

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("users.id", name="fk_car_user_id"),
        nullable=False,
    )
    user: Mapped["User"] = relationship(back_populates="cars")
