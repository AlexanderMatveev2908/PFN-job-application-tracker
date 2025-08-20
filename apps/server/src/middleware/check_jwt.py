from typing import TypedDict
from fastapi import Request
from sqlalchemy import select

from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.tokens.jwt import check_jwt
from src.models.token import PayloadT
from src.models.user import User, UserDcT


class CheckJwtMdwReturnT(TypedDict):
    decoded: PayloadT
    user_d: UserDcT


async def check_check_jwt_mdw(req: Request) -> CheckJwtMdwReturnT:
    splitted = [
        x.strip()
        for x in req.headers.get("authorization", "").split("Bearer ")
        if x.strip()
    ]

    if not (token := (splitted[0] if splitted else None)):
        raise ErrAPI(msg="ACCESS_TOKEN_NOT_PROVIDED", status=401)

    decoded: PayloadT = check_jwt(token)

    async with db_trx() as trx:
        us = (
            await trx.execute(
                select(User).where(User.id == decoded["user_id"])
            )
        ).scalar_one_or_none()

        if not us:
            raise ErrAPI(msg="user not found", status=404)

        print(us.to_d())

        return {}
