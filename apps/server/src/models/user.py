import asyncio
import concurrent.futures
from argon2 import PasswordHasher
import concurrent
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, validates
from src.decorators.err import ErrAPI
from src.lib.logger import clg
from src.models.root import RootTable

PH = PasswordHasher(
    time_cost=3, memory_cost=64 * 1024, parallelism=1, hash_len=32, salt_len=16
)

HASH_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=2)


class User(RootTable):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    terms: Mapped[bool] = mapped_column(Boolean, nullable=False)

    @validates("terms")
    def check_terms(self, k: str, v: bool) -> bool:
        if v is not True:
            raise ErrAPI(msg="User must accepts terms", status=422)

        return v

    async def set_pwd(self, plain: str) -> None:
        loop = asyncio.get_running_loop()

        self.password = await loop.run_in_executor(HASH_POOL, PH.hash, plain)

    async def check_pwd(self, plain: str) -> bool:
        loop = asyncio.get_running_loop()

        try:
            return await loop.run_in_executor(
                HASH_POOL, PH.verify, self.password, plain
            )
        except Exception as err:
            clg(err, ttl="err check pwd")
            return False
