import asyncio
import json
from typing import cast
from fastapi import Depends, Request
from src.__dev_only.payloads import get_payload_register
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.auth.middleware.register import RegisterFormT, register_mdw
from src.features.test.lib.idx import get_query_token_t
from src.features.test.services.tokens_health import (
    tokens_health_svc,
)
from src.lib.cookies import gen_refresh_cookie
from src.lib.data_structure import dest_d, pick
from src.lib.etc import parse_bd
from src.lib.s3.post import upload_w3
from src.lib.system import del_vid
from src.lib.tokens.cbc_hmac import check_cbc_hmac_with_us, gen_cbc_hmac
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.lib.tokens.jwe import check_jwe_with_us
from src.lib.tokens.jwt import check_jwt_lib
from src.models.token import GenTokenReturnT, TokenT
from src.models.user import User


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
    req: Request, user_data: RegisterFormT = Depends(register_mdw)
) -> ResAPI:

    expired: list[str] = req.state.parsed_q.get("expired")

    if expired is None:
        expired = []
    elif isinstance(expired, str):
        expired = [expired]

    res = await tokens_health_svc(
        user_data, token_t=get_query_token_t(req), expired=expired
    )

    return ResAPI.ok_200(
        **pick(res, keys_off=["refresh_token"]),
        cookies=[gen_refresh_cookie(refresh_token=res["refresh_token"])],
    )


async def tokens_expired_ctrl(
    req: Request, user_data: RegisterFormT = Depends(register_mdw)
) -> ResAPI:

    expired: list[str] = req.state.parsed_q.get("expired")

    if expired is None:
        expired = []
    elif isinstance(expired, str):
        expired = [expired]

    res = await tokens_health_svc(
        user_data,
        token_t=get_query_token_t(req),
        reverse=not expired,
        expired=expired,
    )

    return ResAPI.ok_200(
        **res, cookies=[gen_refresh_cookie(refresh_token=res["refresh_token"])]
    )


async def get_err_ctrl(req: Request) -> ResAPI:
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

    return ResAPI.ok_200(payload=payload)


async def get_verified_user_ctrl(req: Request) -> ResAPI:
    payload = get_payload_register()
    filtered = pick(obj=cast(dict, payload), keys_off=["confirm_password"])

    bd = await req.json()
    token_t = TokenT(bd["cbc_hmac_t"])
    expired = bd["expired"]

    async with db_trx() as trx:
        user = User(**filtered, is_verified=True)

        trx.add(user)
        await trx.flush([user])
        await trx.refresh(user)

        tokens_sessions: TokensSessionsReturnT = await gen_tokens_session(
            trx=trx, user_id=user.id, expired=expired
        )
        cbc_res: GenTokenReturnT = await gen_cbc_hmac(
            token_t=token_t,
            trx=trx,
            user_id=user.id,
            reverse="cbc_hmac" in expired,
        )

        return ResAPI.ok_201(
            cbc_hmac_token=cbc_res["client_token"],
            access_token=tokens_sessions["access_token"],
            user=user.to_d(),
            payload=payload,
            cookies=[
                gen_refresh_cookie(
                    tokens_sessions["result_jwe"]["client_token"]
                )
            ],
        )
