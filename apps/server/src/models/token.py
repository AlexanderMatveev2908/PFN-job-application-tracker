from enum import Enum
from typing import Any, TypedDict
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

from src.models.user import UserDcT


class TokenT(Enum):
    REFRESH = "REFRESH"
    CONF_EMAIL = "CONF_EMAIL"
    RECOVER_PWD = "RECOVER_PWD"
    CHANGE_EMAIL = "CHANGE_EMAIL"
    CHANGE_EMAIL_2FA = "CHANGE_EMAIL_2FA"
    CHANGE_PWD = "CHANGE_PWD"
    MANAGE_ACC = "MANAGE_ACC"
    LOGIN_2FA = "LOGIN_2FA"
    MANAGE_ACC_2FA = "MANAGE_ACC_2FA"


class AlgT(Enum):
    AES_CBC_HMAC_SHA256 = "AES-CBC-HMAC-SHA256"
    RSA_OAEP_256_A256GCM = "RSA-OAEP-256-A256GCM"
    HMAC_SHA256 = "HMAC-SHA256"


class PayloadTokenT(
    TypedDict,
):
    user_id: str


PayloadT = dict[str, Any] | PayloadTokenT


class TokenDct(TypedDict):
    id: str
    user_id: str
    token_t: TokenT
    alg: AlgT
    hashed: str
    exp: int


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

    hashed: Mapped[bytes] = mapped_column(LargeBinary(32), nullable=False)

    exp: Mapped[int] = mapped_column(BigInteger, nullable=False)

    user = relationship("User", back_populates="tokens")


class GenTokenReturnT(TypedDict):
    client_token: str
    server_token: Token


class CheckTokenReturnT(TypedDict):
    token_d: TokenDct
    decrypted: PayloadT


class CheckTokenWithUsReturnT(TypedDict):
    token_d: TokenDct
    decrypted: PayloadT
    user_d: UserDcT
