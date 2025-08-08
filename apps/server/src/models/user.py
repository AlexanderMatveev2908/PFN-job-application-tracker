from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String
from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column,
    relationship,
)
from src.models.root import RootTable
from .job import Job

Base = declarative_base()

if TYPE_CHECKING:
    # from .company import Company
    from .car import Car


class User(RootTable):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    jobs: Mapped[List["Job"]] = relationship(
        back_populates="user",
    )

    cars: Mapped[List["Car"]] = relationship(back_populates="user")
