from typing import cast
from fastapi import Depends, Request
from fastapi.responses import JSONResponse, StreamingResponse

from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.features.user.services.TFA import TFA_svc
from src.features.user.services.TFA_zip import TFA_zip_svc
from src.lib.combo.token_mail import gen_token_send_email_svc
from src.lib.db.idx import get_us_by_email, get_us_by_id
from src.lib.validators.idx import EmailFormT, PwdFormT
from src.middleware.combo.idx import (
    ComboCheckJwtCbcBodyReturnT,
    combo_check_jwt_cbc_hmac_body_mdw,
)
from src.models.token import TokenT
from src.models.user import User


async def change_pwd_ctrl(
    req: Request,
    result_combo: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            model=PwdFormT, token_t=TokenT.MANAGE_ACC, check_jwt=True
        )
    ),
) -> JSONResponse:

    async with db_trx() as trx:
        us = await get_us_by_id(
            trx=trx,
            us_id=result_combo["cbc_hmac_result"]["decrypted"]["user_id"],
        )
        new_pwd = result_combo["body"]["password"]

        if await us.check_pwd(plain=new_pwd):
            return ResAPI(req).err_400(
                msg="new password must be different from old one",
            )

        await cast(User, us).set_pwd(plain=new_pwd)

        return ResAPI(req).ok_200(msg="password updated")


async def change_email_ctrl(
    req: Request,
    combo_result: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=True, token_t=TokenT.MANAGE_ACC, model=EmailFormT
        )
    ),
) -> JSONResponse:

    async with db_trx() as trx:
        if (
            combo_result["body"]["email"]
            == combo_result["cbc_hmac_result"]["user_d"]["email"]
        ):
            return ResAPI(req).err_400(
                msg="new email can not be same as old one"
            )

        existing = await get_us_by_email(
            must_exists=False, trx=trx, email=combo_result["body"]["email"]
        )

        if existing:
            return ResAPI(req).err_409(
                msg="a user with this email already exists"
            )

        us = cast(
            User,
            await get_us_by_id(
                trx, combo_result["cbc_hmac_result"]["decrypted"]["user_id"]
            ),
        )
        us.tmp_email = combo_result["body"]["email"]

        await gen_token_send_email_svc(
            trx=trx,
            us_d=combo_result["cbc_hmac_result"]["user_d"],
            token_t=TokenT.CHANGE_EMAIL,
            email_to=combo_result["body"]["email"],
        )

        return ResAPI(req).ok_200(msg="email sent to new address")


async def TFA_ctrl(
    req: Request,
    result_combo: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=True, token_t=TokenT.MANAGE_ACC
        )
    ),
) -> JSONResponse:

    async with db_trx() as trx:
        result_svc = await TFA_svc(trx=trx, result_combo=result_combo)

        return ResAPI(req).ok_200(
            totp_secret=result_svc["secret_result"]["secret"],
            backup_codes=result_svc["backup_codes_result"][
                "backup_codes_client"
            ],
            totp_secret_qrcode=result_svc["qrcode_result"]["base_64"],
        )


async def TFA_zip_ctrl(
    req: Request,
    result_combo: ComboCheckJwtCbcBodyReturnT = Depends(
        combo_check_jwt_cbc_hmac_body_mdw(
            check_jwt=True, token_t=TokenT.MANAGE_ACC
        )
    ),
) -> StreamingResponse:
    async with db_trx() as trx:
        result_svc = await TFA_svc(trx=trx, result_combo=result_combo)

        codes: list[str] = result_svc["backup_codes_result"][
            "backup_codes_client"
        ]

        buf = await TFA_zip_svc(
            backup_codes=codes,
            binary_qr_code=result_svc["qrcode_result"]["binary"],
            totp_secret=result_svc["secret_result"]["secret"],
        )

        return StreamingResponse(
            buf,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=2FA.zip"},
        )
