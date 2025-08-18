import uuid
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.token import Token, TokenT


async def clear_old_tokens(
    trx: AsyncSession, user_id: uuid.UUID | str
) -> None:
    await trx.execute(
        delete(Token).where(
            (Token.token_t.in_([TokenT.REFRESH, TokenT.CONF_EMAIL]))
            & (Token.user_id == user_id)
        )
    )
