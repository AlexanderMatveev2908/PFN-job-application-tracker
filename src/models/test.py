from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from src.models.root import RootTable


class Test(RootTable):
    __tablename__ = "tests"

    value: Mapped[str] = mapped_column(String(50), nullable=False)
