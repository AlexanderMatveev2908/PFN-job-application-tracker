import asyncio
import json
from fastapi import Depends, Request
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.auth.middleware.register import RegisterFormT, register_mdw
from src.features.test.services.tokens_expired import tokens_expired_svc
from src.features.test.services.tokens_health import (
    tokens_health_svc,
)
from src.lib.data_structure import dest_d
from src.lib.etc import parse_bd
from src.lib.s3.post import upload_w3
from src.lib.system import del_vid
from src.lib.tokens.cbc_hmac import check_cbc_hmac
from src.lib.tokens.jwe import check_jwe
from src.lib.tokens.jwt import check_jwt


async def post_form_ctrl(req: Request) -> ResAPI:

    parsed_f = req.state.parsed_f

    images = parsed_f["images"]

    uploaded_images = await asyncio.gather(*(upload_w3(img) for img in images))

    uploaded_video = await upload_w3(parsed_f["video"])

    del_vid(parsed_f)

    return ResAPI.ok_201(
        uploaded_images=uploaded_images, uploaded_video=uploaded_video
    )


async def post_msg_ctrl(req: Request) -> ResAPI:

    b = (json.loads(await req.body())).get("msg", None)

    if isinstance(b, str) and len(b.strip()):
        return ResAPI.ok_200(msg="✅ msg received ☎️")

    return ResAPI.ok_200()


async def tokens_health_ctrl(
    _: Request, user_data: RegisterFormT = Depends(register_mdw)
) -> ResAPI:

    res = await tokens_health_svc(user_data)

    return ResAPI.ok_200(**res)


async def tokens_expired_ctrl(
    _: Request, user_data: RegisterFormT = Depends(register_mdw)
) -> ResAPI:
    res = await tokens_expired_svc(user_data)

    return ResAPI.ok_200(**res)


async def get_err_expired_ctrl(req: Request) -> ResAPI:
    data = await parse_bd(req)

    act, token = dest_d(data, keys=["act", "token"])

    async with db_trx() as trx:
        match act:
            case "JWT":
                payload = check_jwt(token)
            case "JWE":
                payload = (
                    await check_jwe(
                        token=token,
                        trx=trx,
                    )
                )["decrypted"]
            case "CBC_HMAC":
                payload = (await check_cbc_hmac(token=token, trx=trx))[
                    "decrypted"
                ]
            case _:
                raise ErrAPI(msg="unknown action", status=400)

    return ResAPI.ok_200(payload=(payload))
