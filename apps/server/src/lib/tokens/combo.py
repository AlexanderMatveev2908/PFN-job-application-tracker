from typing import Any
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.lib.tokens.jwe import gen_jwe
from src.lib.tokens.jwt import gen_jwt
from src.models.token import GenTokenReturnT


TokensSessionsReturnT = tuple[str, GenTokenReturnT]


async def gen_tokens_session(
    user_id: str | uuid.UUID,
    trx: AsyncSession,
    reverse: bool = False,
    **kwargs: Any,
) -> TokensSessionsReturnT:
    result_jwe = await gen_jwe(user_id=user_id, trx=trx, reverse=reverse)
    access_token: str = gen_jwt(user_id, reverse=reverse)

    return (access_token, result_jwe)
