from sqlalchemy import String
from src.models.root import RootTable
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .job import Job

# if TYPE_CHECKING:
# from .user import User


class Company(RootTable):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    jobs: Mapped[list["Job"]] = relationship(
        back_populates="company",
    )
