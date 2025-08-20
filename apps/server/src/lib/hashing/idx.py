import asyncio
import concurrent.futures
from argon2 import PasswordHasher
import concurrent


PH = PasswordHasher(
    time_cost=3, memory_cost=64 * 1024, parallelism=1, hash_len=32, salt_len=16
)

HASH_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=2)


async def hash_pwd(plain: str) -> str:
    loop = asyncio.get_running_loop()

    return await loop.run_in_executor(HASH_POOL, PH.hash, plain)


async def check_pwd(hashed: str, plain: str) -> bool:
    loop = asyncio.get_running_loop()

    try:
        return await loop.run_in_executor(HASH_POOL, PH.verify, hashed, plain)
    except Exception:
        return False
