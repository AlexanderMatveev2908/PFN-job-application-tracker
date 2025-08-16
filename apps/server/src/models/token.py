from enum import Enum
import uuid

from sqlalchemy import (
    UUID,
    BigInteger,
    ForeignKey,
    Enum as PgEnum,
    LargeBinary,
)
from src.models.root import RootTable
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TokenT(Enum):
    REFRESH = "REFRESH"
    CONF_EMAIL = "CONF_EMAIL"
    RECOVER_PWD = "RECOVER_PWD"
    CHANGE_EMAIL = "CHANGE_EMAIL"
    CHANGE_PWD = "CHANGE_PWD"
    MANAGE_ACC = "MANAGE_ACC"


class Token(RootTable):
    __tablename__ = "tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", name="fk_tokens_user", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token_t: Mapped[TokenT] = mapped_column(
        PgEnum(
            TokenT,
            name="token_type",
        ),
        nullable=False,
    )

    hashed: Mapped[bytes] = mapped_column(
        LargeBinary(32), unique=True, nullable=False
    )

    exp: Mapped[int] = mapped_column(BigInteger, nullable=False)

    user = relationship("User", back_populates="tokens")
