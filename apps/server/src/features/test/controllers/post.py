import asyncio
import json
from fastapi import Request
from fastapi.responses import Response
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.test.lib.idx import get_optional_payload, get_query_token_t
from src.features.test.services.tokens_health import (
    tokens_health_svc,
)
from src.features.user.services.TFA_zip import TFA_zip_svc
from src.lib.TFA.backup import gen_backup_codes
from src.lib.TFA.totp import GenTotpSecretReturnT, gen_totp_secret
from src.lib.algs.fernet import gen_fernet
from src.lib.cookies import gen_refresh_cookie
from src.lib.data_structure import dest_d, pick
from src.lib.etc import parse_bd
from src.lib.qrcode.idx import GenQrcodeReturnT, gen_qrcode
from src.lib.s3.post import upload_w3
from src.lib.system import del_vid
from src.lib.tokens.cbc_hmac import check_cbc_hmac_with_us, gen_cbc_hmac
from src.lib.tokens.combo import gen_tokens_session
from src.lib.tokens.jwe import check_jwe_with_us
from src.lib.tokens.jwt import check_jwt_lib
from src.models.token import TokenT
from src.models.user import User


async def post_form_ctrl(req: Request) -> Response:

    parsed_f = req.state.parsed_f

    images = parsed_f["images"]

    uploaded_images = await asyncio.gather(*(upload_w3(img) for img in images))

    uploaded_video = await upload_w3(parsed_f["video"])

    del_vid(parsed_f)

    return ResAPI(req).ok_201(
        uploaded_images=uploaded_images, uploaded_video=uploaded_video
    )


async def post_msg_ctrl(req: Request) -> Response:

    b = (json.loads(await req.body())).get("msg", None)

    if isinstance(b, str) and len(b.strip()):
        return ResAPI(req).ok_200(
            msg="ok",
        )

    return ResAPI(req).err_400()


async def tokens_health_ctrl(
    req: Request,
) -> Response:

    payload = await get_optional_payload(req)

    res = await tokens_health_svc(
        payload, token_t=get_query_token_t(req), parsed_q=req.state.parsed_q
    )

    return ResAPI(
        req, cookies=[gen_refresh_cookie(refresh_token=res["refresh_token"])]
    ).ok_200(
        **pick(res, keys_off=["refresh_token"]),
    )


async def get_err_ctrl(req: Request) -> Response:
    data = await parse_bd(req)

    act, token = dest_d(data, keys=["act", "token"])

    async with db_trx() as trx:
        match act:
            case "JWT":
                payload = check_jwt_lib(token)
            case "JWE":
                payload = (
                    await check_jwe_with_us(
                        token=token,
                        trx=trx,
                    )
                )["decrypted"]
            case "CBC_HMAC":
                payload = (
                    await check_cbc_hmac_with_us(
                        token=token, trx=trx, token_t=get_query_token_t(req)
                    )
                )["decrypted"]
            case _:
                raise ErrAPI(msg="unknown action", status=400)

    return ResAPI(req).ok_200(payload=payload)


async def get_us_2FA_ctrl(
    req: Request,
) -> Response:

    filtered = await get_optional_payload(req)

    q = req.state.parsed_q
    empty_codes = q.get("empty_codes")
    expired: list[str] = q.get("expired") or []

    if isinstance(expired, str):
        expired = [expired]

    try:
        token_t = TokenT(q.get("cbc_hmac_t"))

    except Exception:
        raise ErrAPI(msg="invalid cbc_hmac_type", status=422)

    async with db_trx() as trx:

        us = User(**filtered, is_verified=True)
        await us.set_pwd(filtered["password"])

        trx.add(us)
        await trx.flush([us])
        await trx.refresh(us)

        secret_result: GenTotpSecretReturnT = gen_totp_secret(
            user_email=us.email
        )
        us.totp_secret = gen_fernet(txt=secret_result["secret"])

        backup_codes: list[str] = []
        if not empty_codes:
            backup_codes = (await gen_backup_codes(trx, us_id=us.id))[
                "backup_codes_client"
            ]

        tokens_session = await gen_tokens_session(
            trx=trx, user_id=us.id, expired=expired
        )

        cbc_hmac_res = await gen_cbc_hmac(
            trx=trx,
            token_t=token_t,
            user_id=us.id,
            reverse="cbc_hmac" in expired,
        )

        qrcode_result: GenQrcodeReturnT = gen_qrcode(uri=secret_result["uri"])

        await TFA_zip_svc(
            backup_codes=backup_codes,
            binary_qr_code=qrcode_result["binary"],
            totp_secret=secret_result["secret"],
        )

        return ResAPI(
            req,
            cookies=[
                gen_refresh_cookie(
                    tokens_session["result_jwe"]["client_token"]
                )
            ],
        ).ok_200(
            payload=filtered,
            user=us,
            totp_secret=secret_result["secret"],
            backup_codes=backup_codes,
            access_token=tokens_session["access_token"],
            cbc_hmac_token=cbc_hmac_res["client_token"],
        )
