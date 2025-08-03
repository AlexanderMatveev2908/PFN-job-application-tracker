import uuid
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Column, ForeignKey
from sqlmodel import Field, Relationship
from src.models.root import RootTable
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

if TYPE_CHECKING:
    from .company import Company
    from .user import User


class Job(RootTable, table=True):
    __tablename__ = "jobs"  # type: ignore

    title: str = Field(sa_column=Column(String(50), nullable=False))

    company_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("companies.id", name="fk_job_company_id"),
            nullable=False,
        )
    )

    user_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("users.id", name="fk_job_user_id"),
            nullable=False,
        )
    )

    company: Optional["Company"] = Relationship(back_populates="jobs")
    user: Optional["User"] = Relationship(back_populates="jobs")


# from typing import TYPE_CHECKING
# import uuid
# from sqlalchemy import ForeignKey, String
# from src.models.root import RootTable
# from sqlalchemy.orm import Mapped, mapped_column, relationship


# if TYPE_CHECKING:
#     from .user import User
#     from .company import Company


# class Job(RootTable):
#     __tablename__ = "jobs"

#     title: Mapped[str] = mapped_column(String(50), nullable=False)

#     company_id: Mapped[uuid.UUID] = mapped_column(
#         ForeignKey("companies.id", name="fk_job_company_id"), nullable=False
#     )
#     user_id: Mapped[uuid.UUID] = mapped_column(
#         ForeignKey("users.id", name="fk_job_user_id"), nullable=False
#     )

#     company: Mapped["Company"] = relationship(back_populates="jobs")
#     user: Mapped["User"] = relationship(back_populates="jobs")
