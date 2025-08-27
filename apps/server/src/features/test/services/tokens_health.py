from typing import Any, cast
import uuid

from sqlalchemy import delete
from src.conf.db import db_trx
from src.features.auth.middleware.register import RegisterFormT
from src.lib.data_structure import parse_id, pick
from src.lib.db.idx import get_us_by_email
from src.lib.etc import grab
from src.lib.tokens.cbc_hmac import (
    gen_cbc_hmac,
)
from src.lib.tokens.combo import gen_tokens_session
from src.models.token import GenTokenReturnT, Token, TokenT
from src.models.user import User


async def tokens_health_svc(
    user_data: RegisterFormT,
    token_t: TokenT,
    parsed_q: dict[str, Any],
) -> Any:
    async with db_trx() as trx:

        expired: str | list[str] | None = parsed_q.get("expired")
        verify_user: bool = bool(parsed_q.get("verify_user"))

        if expired is None:
            expired = []
        elif isinstance(expired, str):
            expired = [expired]

        us = await get_us_by_email(trx, user_data["email"], must_exists=False)

        if not us:
            data = pick(obj=cast(dict, user_data), keys_off=["password"])
            user_id = parse_id(uuid.uuid4())
            plain_pwd = user_data["password"]

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
            "refresh_token": grab(result_tokens, "client_token"),
            "cbc_hmac_token": result_cbc_hmac["client_token"],
        }
