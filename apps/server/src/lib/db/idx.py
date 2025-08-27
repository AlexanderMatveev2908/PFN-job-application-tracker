import uuid
from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.decorators.err import ErrAPI
from src.models.token import Token, TokenT
from src.models.user import User


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


async def del_token_by_t(
    trx: AsyncSession, us_id: str | uuid.UUID, token_t: TokenT
) -> None:
    await trx.execute(
        delete(Token).where(
            (Token.user_id == us_id) & (Token.token_t == token_t)
        )
    )
