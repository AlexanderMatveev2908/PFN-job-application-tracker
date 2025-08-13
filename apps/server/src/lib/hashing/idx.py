import asyncio
from argon2 import PasswordHasher


async def hash_pwd(txt: str) -> str:
    ph = PasswordHasher()
    return await asyncio.to_thread(ph.hash, txt)


async def check_pwd(hashed: str, plain: str) -> bool:
    try:
        ph = PasswordHasher()
        return await asyncio.to_thread(ph.verify, hashed, plain)
    except Exception:
        return False
