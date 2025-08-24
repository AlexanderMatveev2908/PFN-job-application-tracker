from typing import TypedDict
from src.decorators.err import ErrAPI
from src.lib.TFA.backup import GenBackupCodesReturnT, gen_backup_codes
from src.lib.TFA.totp import GenTotpSecretReturnT, gen_totp_secret
from src.lib.algs.fernet import gen_fernet
from src.lib.db.idx import get_us_by_id
from src.lib.qrcode.idx import GenQrcodeReturnT, gen_qrcode
from src.middleware.combo.idx import ComboCheckJwtCbcBodyReturnT
from sqlalchemy.ext.asyncio import AsyncSession


class TFASVCReturnT(TypedDict):
    secret_result: GenTotpSecretReturnT
    qrcode_result: GenQrcodeReturnT
    backup_codes_result: GenBackupCodesReturnT


async def TFA_svc(
    trx: AsyncSession, result_combo: ComboCheckJwtCbcBodyReturnT
) -> TFASVCReturnT:
    us = await get_us_by_id(
        trx=trx, us_id=result_combo["cbc_hmac_result"]["user_d"]["id"]
    )

    if not us.is_verified:
        raise ErrAPI(msg="user must be verified to set up 2FA", status=400)

    if us.totp_secret:
        raise ErrAPI(msg="user already have 2FA set up", status=409)

    secret_result: GenTotpSecretReturnT = gen_totp_secret(user_email=us.email)

    us.totp_secret = gen_fernet(txt=secret_result["secret"])

    qrcode_result: GenQrcodeReturnT = gen_qrcode(uri=secret_result["uri"])

    backup_codes_result: GenBackupCodesReturnT = await gen_backup_codes(
        trx, us_id=us.id
    )

    return {
        "secret_result": secret_result,
        "qrcode_result": qrcode_result,
        "backup_codes_result": backup_codes_result,
    }
