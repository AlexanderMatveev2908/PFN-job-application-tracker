import uuid
from sqlalchemy import UUID, ForeignKey, String
from src.models.root import RootTable
from sqlalchemy.orm import MappedColumn, mapped_column, relationship


class BackupCode(RootTable):
    __tablename__ = "backup_codes"

    code: MappedColumn[str] = mapped_column(String(250), nullable=False)

    user_id: MappedColumn[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id", name="fk_backup_codes_user", ondelete="CASCADE"
        ),
        index=True,
    )

    user = relationship("User", back_populates="backup_codes")
