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
    from .company import Company


class User(RootTable):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )

    jobs: Mapped[list["Job"]] = relationship(
        back_populates="user",
    )
    companies: Mapped[list["Company"]] = relationship(
        secondary="jobs", back_populates="users", viewonly=True
    )
