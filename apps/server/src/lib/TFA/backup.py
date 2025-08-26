import os
from typing import TypedDict, cast
import uuid

from sqlalchemy import select, text
from src.decorators.err import ErrAPI
from src.lib.hashing.idx import check_argon, hash_argon
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.backup_code import BackupCode


class GenBackupCodesReturnT(TypedDict):
    backup_codes_client: list[str]
    backup_codes_server: list[BackupCode]


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

    return {"backup_codes_client": codes, "backup_codes_server": backup_codes}


class CheckBackupCodeReturnT(TypedDict):
    backup_code_server: BackupCode
    backup_codes_left: int


async def check_backup_code(
    trx: AsyncSession, us_id: str | uuid.UUID, backup_code: str
) -> CheckBackupCodeReturnT:
    backup_codes = cast(
        list[BackupCode],
        (
            await trx.execute(
                select(BackupCode).from_statement(
                    text(
                        """
                            SELECT *
                                FROM backup_codes bc
                                WHERE bc.user_id = :user_id
                            """
                    )
                ),
                {"user_id": us_id},
            )
        )
        .scalars()
        .all(),
    )

    if not backup_codes:
        raise ErrAPI(msg="user has no backup codes", status=401)

    found_code: BackupCode | None = None

    for bc in backup_codes:
        if await check_argon(
            hashed=bc.code,
            plain=backup_code,
        ):
            found_code = bc
            break

    if not found_code:
        raise ErrAPI(msg="backup_code_invalid", status=401)

    await trx.delete(found_code)

    return {
        "backup_code_server": found_code,
        "backup_codes_left": len(backup_codes) - 1,
    }
