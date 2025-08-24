import os
from typing import TypedDict
import uuid
from src.lib.hashing.idx import hash_argon
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.backup_code import BackupCode


class GenBackupCodesReturnT(TypedDict):
    codes: list[str]
    backup_codes_db: list[BackupCode]


async def gen_backup_codes(
    trx: AsyncSession, us_id: str | uuid.UUID
) -> GenBackupCodesReturnT:
    codes: list[str] = []
    hashed_codes: list[str] = []

    for _ in range(8):
        code = os.urandom(4).hex().upper()
        formatted = f"{code[:4]}-{code[4:]}"

        codes.append(formatted)
        hashed_codes.append(await hash_argon(plain=formatted))

    backup_codes: list[BackupCode] = list(
        map(
            lambda h: BackupCode(**{"user_id": us_id, "code": h}), hashed_codes
        )
    )
    trx.add_all(backup_codes)
    await trx.flush(backup_codes)
    for bc in backup_codes:
        await trx.refresh(bc)

    return {"codes": codes, "backup_codes_db": backup_codes}
