from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column,
    relationship,
)
from src.models.root import RootTable

Base = declarative_base()

if TYPE_CHECKING:
    from .job import Job


class User(RootTable):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)

    email: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )

    job: Mapped["Job"] = relationship(back_populates="user", uselist=False)
