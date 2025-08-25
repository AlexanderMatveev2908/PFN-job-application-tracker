from typing import cast
from fastapi import Depends, Request
from src.__dev_only.payloads import get_payload_register
from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.lib.cookies import gen_refresh_cookie
from src.lib.data_structure import pick
from src.lib.tokens.cbc_hmac import gen_cbc_hmac
from src.lib.tokens.combo import TokensSessionsReturnT, gen_tokens_session
from src.middleware.check_jwt import check_jwt_search_us_mdw
from src.models.token import GenTokenReturnT, TokenT
from src.models.user import User, UserDcT


async def get_msg_ctrl(req: Request) -> ResAPI:

    return ResAPI.ok_200(
        msg="✅ get request ☎️",
    )


async def get_protected_data_ctrl(
    _: Request, us: UserDcT = Depends(check_jwt_search_us_mdw)
) -> ResAPI:
    return ResAPI.ok_200(msg="protected data 👻")


async def get_verified_user_ctrl(req: Request) -> ResAPI:
    payload = get_payload_register()
    filtered = pick(obj=cast(dict, payload), keys_off=["confirm_password"])

    token_t = TokenT(req.query_params.get("cbc_hmac_t"))

    expired_raw: str | list[str] | None = req.state.parsed_q.get("expired")

    if expired_raw is None:
        expired: list[str] = []
    elif isinstance(expired_raw, list):
        expired = expired_raw
    else:
        expired = [expired_raw]

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
