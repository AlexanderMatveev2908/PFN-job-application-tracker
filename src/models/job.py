from typing import TYPE_CHECKING
import uuid
from sqlalchemy import ForeignKey, String
from src.models.root import RootTable
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from .user import User


class Job(RootTable):
    __tablename__ = "jobs"

    title: Mapped[str] = mapped_column(String(50), nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="job", uselist=False)
