from typing import cast
from fastapi import Request
from sqlalchemy import select

from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.tokens.jwt import check_jwt_lib
from src.models.token import PayloadT
from src.models.user import User, UserDcT


def extract_jwt(req: Request) -> str:
    splitted = [
        x.strip()
        for x in req.headers.get("authorization", "").split("Bearer ")
        if x.strip()
    ]

    if not (token := (splitted[0] if splitted else None)):
        raise ErrAPI(msg="ACCESS_TOKEN_NOT_PROVIDED", status=401)

    return token


def check_jwt_mdw(req: Request) -> PayloadT:

    decoded: PayloadT = check_jwt_lib(extract_jwt(req))

    return decoded


async def check_jwt_search_us_mdw(req: Request) -> UserDcT:
    decoded: PayloadT = check_jwt_mdw(req)

    async with db_trx() as trx:
        us = (
            await trx.execute(
                select(User).where(User.id == decoded["user_id"])
            )
        ).scalar_one_or_none()

        if not us:
            raise ErrAPI(msg="user not found", status=404)

        return cast(UserDcT, us.to_d())
