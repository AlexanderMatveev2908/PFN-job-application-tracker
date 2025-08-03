from typing import TYPE_CHECKING, List
from sqlalchemy import String, Column
from sqlmodel import Field, Relationship
from src.models.root import RootTable

if TYPE_CHECKING:
    from .user import User
    from .job import Job


class Company(RootTable, table=True):
    __tablename__ = "companies"  # type: ignore

    name: str = Field(sa_column=Column(String(50), nullable=False, index=True))

    jobs: List["Job"] = Relationship(back_populates="company")

    users: List["User"] = Relationship(
        back_populates="companies",
        sa_relationship_kwargs={"secondary": "jobs", "viewonly": True},
    )


# from typing import TYPE_CHECKING
# from sqlalchemy import String
# from src.models.root import RootTable
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from .job import Job

# if TYPE_CHECKING:
#     from .user import User


# class Company(RootTable):
#     __tablename__ = "companies"

#     name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

#     jobs: Mapped[list["Job"]] = relationship(
#         back_populates="company",
#     )
#     users: Mapped[list["User"]] = relationship(
#         secondary=Job.__table__,
#         back_populates="companies",
#         viewonly=True,
#     )
