from sqlalchemy import Column, String
from sqlmodel import Field
from src.models.root import RootTable


class Test(RootTable, table=True):
    __tablename__ = "tests"  # type: ignore

    value: str = Field(sa_column=Column(String(50), nullable=False))


# from sqlalchemy import String
# from sqlalchemy.orm import (
#     Mapped,
#     mapped_column,
# )
# from src.models.root import RootTable


# class Test(RootTable):
#     __tablename__ = "tests"

#     value: Mapped[str] = mapped_column(String(50), nullable=False)
