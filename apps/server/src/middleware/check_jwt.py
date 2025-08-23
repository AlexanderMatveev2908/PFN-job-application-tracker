from typing import cast
from fastapi import Request

from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.db.idx import get_us_by_id
from src.lib.tokens.jwt import check_jwt_lib
from src.models.token import PayloadT
from src.models.user import UserDcT


def extract_jwt(req: Request) -> str:
    splitted = [
        x.strip()
        for x in req.headers.get("authorization", "").split("Bearer")
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
        us = await get_us_by_id(trx=trx, us_id=decoded["user_id"])
        return cast(UserDcT, us.to_d())
