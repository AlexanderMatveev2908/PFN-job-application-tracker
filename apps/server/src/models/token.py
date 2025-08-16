from enum import Enum
from typing import TypedDict
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


class AlgT(Enum):
    AES_CBC_HMAC_SHA256 = "AES-CBC-HMAC-SHA256"
    RSA_OAEP_256_A256GCM = "RSA-OAEP-256-A256GCM"
    HMAC_SHA256 = "HMAC-SHA256"


class PayloadTokenT(TypedDict):
    user_id: str


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

    alg: Mapped[AlgT] = mapped_column(PgEnum(AlgT, name="alg_type"))

    hashed: Mapped[bytes] = mapped_column(LargeBinary(32), nullable=True)

    exp: Mapped[int] = mapped_column(BigInteger, nullable=False)

    user = relationship("User", back_populates="tokens")
