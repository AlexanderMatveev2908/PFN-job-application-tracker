from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship
from src.models.root import RootTable
from .job import Job

if TYPE_CHECKING:
    from .car import Car


class User(RootTable, table=True):
    __tablename__ = "users"  # type: ignore

    name: str = Field(sa_column=Column(String(50), nullable=False))
    email: str = Field(
        sa_column=Column(String(50), nullable=False, unique=True, index=True)
    )

    jobs: List["Job"] = Relationship(back_populates="user")
    cars: List["Car"] = Relationship(back_populates="user")


# from typing import TYPE_CHECKING
# from sqlalchemy import String
# from sqlalchemy.orm import (
#     declarative_base,
#     Mapped,
#     mapped_column,
#     relationship,
# )
# from src.models.root import RootTable
# from .job import Job

# Base = declarative_base()

# if TYPE_CHECKING:
#     from .company import Company
#     from .car import Car


# class User(RootTable):
#     __tablename__ = "users"

#     name: Mapped[str] = mapped_column(String(50), nullable=False)
#     email: Mapped[str] = mapped_column(
#         String(50), nullable=False, unique=True, index=True
#     )

#     jobs: Mapped[List["Job"]] = relationship(
#         back_populates="user",
#     )
#     companies: Mapped[List["Company"]] = relationship(
#         secondary=Job.__table__, back_populates="users", viewonly=True
#     )
#     cars: Mapped[List["Car"]] = relationship(back_populates="user")
