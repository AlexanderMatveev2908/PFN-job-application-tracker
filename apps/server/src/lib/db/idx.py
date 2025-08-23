import uuid
from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.decorators.err import ErrAPI
from src.models.token import Token, TokenT
from src.models.user import User


async def clear_old_tokens(
    trx: AsyncSession, user_id: uuid.UUID | str
) -> None:
    await trx.execute(
        delete(Token).where(
            (Token.token_t.in_([TokenT.REFRESH, TokenT.CONF_EMAIL]))
            & (Token.user_id == user_id)
        )
    )


async def get_us_by_id(trx: AsyncSession, us_id: str) -> User:
    us = await trx.get(User, us_id)

    if not us:
        raise ErrAPI(msg="user not found", status=404)

    return us


async def get_us_by_email(
    trx: AsyncSession, email: str, must_exists: bool = True
) -> User | None:
    stmt = select(User).from_statement(
        text("SELECT * FROM users WHERE email = :email")
    )
    us = (await trx.execute(stmt, {"email": email})).scalar_one_or_none()

    if must_exists:
        if not us:
            raise ErrAPI(msg="user not found", status=404)

    return us
