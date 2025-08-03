from typing import TYPE_CHECKING
from sqlalchemy import String
from src.models.root import RootTable
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User
    from .job import Job


class Company(RootTable):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    jobs: Mapped[list["Job"]] = relationship(
        back_populates="company",
    )
    users: Mapped[list["User"]] = relationship(
        secondary="jobs",
        back_populates="companies",
        viewonly=True,
    )
