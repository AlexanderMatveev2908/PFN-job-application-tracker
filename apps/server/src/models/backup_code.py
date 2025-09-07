from typing import TYPE_CHECKING, TypedDict
import uuid
from sqlalchemy import UUID, ForeignKey, String
from src.models.root import RootTable
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User


class BackupCodeDct(TypedDict):
    code: str
    user_id: str


class BackupCode(RootTable):
    __tablename__ = "backup_codes"

    code: Mapped[str] = mapped_column(String(250), nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id", name="fk_backup_codes_user", ondelete="CASCADE"
        ),
        index=True,
    )

    user: Mapped["User"] = relationship("User", back_populates="backup_codes")
