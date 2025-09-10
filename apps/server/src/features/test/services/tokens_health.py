from typing import Any, TypedDict, cast
import uuid

from sqlalchemy import delete
from src.__dev_only.payloads import RegisterPartPayloadT, RegisterPayloadT
from src.conf.db import db_trx
from src.lib.data_structure.etc import pick
from src.lib.data_structure.parsers import parse_id
from src.lib.db.idx import get_us_by_email
from src.lib.tokens.cbc_hmac import (
    gen_cbc_hmac,
)
from src.lib.tokens.combo import gen_tokens_session
from src.models.token import GenTokenReturnT, Token, TokenT
from src.models.user import User


class TokensHealthSvcReturnT(TypedDict):
    payload: RegisterPayloadT
    user: User
    access_token: str
    refresh_token: str
    cbc_hmac_token: str


async def tokens_health_svc(
    payload: RegisterPartPayloadT,
    token_t: TokenT,
    parsed_q: dict[str, Any],
) -> TokensHealthSvcReturnT:
    async with db_trx() as trx:

        expired: str | list[str] | None = parsed_q.get("expired")
        verify_user: bool = bool(parsed_q.get("verify_user"))

        if expired is None:
            expired = []
        elif isinstance(expired, str):
            expired = [expired]

        us = await get_us_by_email(trx, payload["email"], must_exists=False)

        if not us:
            data = pick(obj=cast(dict, payload), keys_off=["password"])
            user_id = parse_id(uuid.uuid4())
            plain_pwd = payload["password"]

            us = User(**data, id=user_id, is_verified=verify_user)
            await us.set_pwd(plain_pwd)
            trx.add(us)
            await trx.flush([us])
            await trx.refresh(us)

        await trx.execute(delete(Token).where(Token.user_id == us.id))

        result_tokens = await gen_tokens_session(
            user_id=us.id, trx=trx, expired=expired
        )

        result_cbc_hmac: GenTokenReturnT = await gen_cbc_hmac(
            user_id=us.id,
            token_t=token_t,
            trx=trx,
            reverse="cbc_hmac" in expired,
        )

        return {
            "user": us,
            "access_token": result_tokens["access_token"],
            "refresh_token": result_tokens["result_jwe"]["client_token"],
            "cbc_hmac_token": result_cbc_hmac["client_token"],
            "payload": {**payload, "confirm_password": payload["password"]},
        }
