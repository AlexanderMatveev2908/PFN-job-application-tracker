from typing import TYPE_CHECKING, List
from sqlalchemy import String
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

    jobs: Mapped[List["Job"]] = relationship(
        back_populates="user",
    )
    # companies: Mapped[List["Company"]] = relationship(
    #     secondary=Job.__table__, back_populates="users", viewonly=True
    # )
    cars: Mapped[List["Car"]] = relationship(back_populates="user")
