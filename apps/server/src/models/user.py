from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, validates
from src.decorators.err import ErrAPI
from src.models.root import RootTable


class User(RootTable):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    terms: Mapped[bool] = mapped_column(Boolean, nullable=False)

    @validates("terms")
    def check_terms(self, k: str, v: bool) -> bool:
        if v is not True:
            raise ErrAPI(msg="User must accepts terms", status=422)

        return v
