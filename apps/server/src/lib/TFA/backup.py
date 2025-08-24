import os
from typing import TypedDict

from src.lib.hashing.idx import hash_argon


class GenBackupCodesReturnT(TypedDict):
    codes: list[str]
    hashed_codes: list[str]


async def gen_backup_codes() -> GenBackupCodesReturnT:
    codes: list[str] = []
    hashed_codes: list[str] = []

    for _ in range(8):
        code = os.urandom(4).hex().upper()
        formatted = f"{code[:4]}-{code[4:]}"

        codes.append(formatted)
        hashed_codes.append(await hash_argon(plain=formatted))

    return {"codes": codes, "hashed_codes": hashed_codes}
