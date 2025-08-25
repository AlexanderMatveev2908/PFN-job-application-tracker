from typing import Any, TypedDict
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.lib.tokens.jwe import gen_jwe
from src.lib.tokens.jwt import gen_jwt
from src.models.token import GenTokenReturnT


class TokensSessionsReturnT(TypedDict):
    access_token: str
    result_jwe: GenTokenReturnT


async def gen_tokens_session(
    user_id: str | uuid.UUID,
    trx: AsyncSession,
    reverse: bool = False,
    expired: list[str] = [],
    **kwargs: Any,
) -> TokensSessionsReturnT:
    access_token: str = gen_jwt(user_id, reverse=reverse or "jwt" in expired)

    result_jwe: GenTokenReturnT = await gen_jwe(
        user_id=user_id, trx=trx, reverse=reverse or "jwe" in expired
    )

    return {"access_token": access_token, "result_jwe": result_jwe}
