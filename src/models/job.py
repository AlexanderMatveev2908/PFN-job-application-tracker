from typing import TYPE_CHECKING
import uuid
from sqlalchemy import ForeignKey, String
from src.models.root import RootTable
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from .user import User
    from .company import Company


class Job(RootTable):
    __tablename__ = "jobs"

    title: Mapped[str] = mapped_column(String(50), nullable=False)

    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id", name="fk_job_company_id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", name="fk_job_user_id"), nullable=False
    )

    company: Mapped["Company"] = relationship(back_populates="jobs")
    user: Mapped["User"] = relationship(back_populates="jobs")
