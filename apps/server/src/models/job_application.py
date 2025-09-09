from enum import Enum
from typing import TYPE_CHECKING, TypedDict
import uuid

from sqlalchemy import (
    UUID,
    BigInteger,
    ForeignKey,
    String,
    Enum as PgEnum,
)
from src.models.root import RootTable
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User


class ApplicationStatusT(Enum):
    APPLIED = "APPLIED"
    UNDER_REVIEW = "UNDER_REVIEW"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"


class JobApplicationDct(TypedDict):
    user_id: str | uuid.UUID
    company_name: str
    position_name: str
    status: ApplicationStatusT
    applied_at: int


class JobApplication(RootTable):
    __tablename__ = "job_applications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id", name="fk_job_applications_user", ondelete="CASCADE"
        ),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="job_applications"
    )

    company_name: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )

    position_name: Mapped[str] = mapped_column(String(100), nullable=True)

    status: Mapped[ApplicationStatusT] = mapped_column(
        PgEnum(ApplicationStatusT, name="application_status_type"),
    )

    applied_at: Mapped[int] = mapped_column(BigInteger, nullable=False)

    notes: Mapped[str] = mapped_column(String(1000), nullable=True)
