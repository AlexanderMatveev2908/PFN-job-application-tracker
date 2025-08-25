from typing import TYPE_CHECKING, Self, TypedDict, cast
from sqlalchemy import Boolean, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from src.decorators.err import ErrAPI
from src.lib.hashing.idx import check_argon, hash_argon
from src.lib.logger import clg
from src.models.root import RootTable


if TYPE_CHECKING:
    from .token import Token
    from .backup_code import BackupCode


class UserDcT(TypedDict):
    id: str
    first_name: str
    last_name: str
    email: str
    password: str
    terms: bool
    is_verified: bool
    totp_secret: str | None


class User(RootTable):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, index=True
    )
    tmp_email: Mapped[str | None] = mapped_column(
        String(254),
        nullable=True,
    )
    password: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    totp_secret: Mapped[bytes | None] = mapped_column(
        LargeBinary, nullable=True
    )
    terms: Mapped[bool] = mapped_column(Boolean, nullable=False)

    tokens: Mapped[list["Token"]] = relationship(
        "Token", back_populates="user"
    )
    backup_codes: Mapped[list["BackupCode"]] = relationship(
        "BackupCode", back_populates="user"
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    @validates("terms")
    def check_terms(self, k: str, v: bool) -> bool:
        if v is not True:
            raise ErrAPI(msg="User must accepts terms", status=422)

        return v

    def toggle_mails(self) -> None:
        self.email = cast(str, self.tmp_email)
        self.tmp_email = None

    async def set_pwd(self, plain: str) -> None:
        self.password = await hash_argon(plain)

    async def check_pwd(self, plain: str) -> bool:

        try:
            return await check_argon(hashed=self.password, plain=plain)
        except Exception as err:
            clg(err, ttl="invalid password")
            return False

    def verify_email(
        self,
    ) -> Self:
        self.is_verified = True

        return self
