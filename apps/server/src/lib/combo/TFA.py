from typing import TypedDict
from src.lib.db.idx import del_token_by_t, get_us_by_id
from src.lib.etc import grab
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.token import TokenT
from src.models.user import User


class Check2FALibReturnT(TypedDict):
    backup_codes_left: int | None
    user: User


async def check_2FA_lib(
    trx: AsyncSession, res_combo: ComboCheckJwtCbcBodyReturnT
) -> Check2FALibReturnT:

    us = await get_us_by_id(trx, grab(res_combo, "user_id"))
    backup_codes_left: int | None = None

    if totp_code := grab(res_combo, "totp_code"):
        us.check_totp(totp_code)
    elif backup_code := (grab(res_combo, "backup_code")):
        backup_codes_left = (await us.check_backup_code(trx, backup_code))[
            "backup_codes_left"
        ]

    await del_token_by_t(
        trx=trx,
        us_id=us.id,
        token_t=TokenT(grab(res_combo, "token_t")),
    )

    return {"user": us, "backup_codes_left": backup_codes_left}
