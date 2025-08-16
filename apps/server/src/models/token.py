from enum import Enum
import uuid

from sqlalchemy import (
    UUID,
    BigInteger,
    Boolean,
    ForeignKey,
    Enum as PgEnum,
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
        PgEnum(TokenT, name="token_type", create_constraint=True),
        nullable=False,
    )

    is_valid: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    exp: Mapped[int] = mapped_column(BigInteger, nullable=False)

    user = relationship("User", back_populates="tokens")
