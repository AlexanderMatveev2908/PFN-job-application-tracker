from typing import Awaitable, Callable, cast
from fastapi import Request

from src.conf.db import db_trx
from src.constants.reg import REG_JWE
from src.decorators.err import ErrAPI
from src.lib.db.idx import get_us_by_id
from src.lib.tokens.jwt import check_jwt_lib
from src.models.token import PayloadT
from src.models.user import User, UserDcT


def extract_jwt(req: Request) -> str:
    splitted = [
        x.strip()
        for x in req.headers.get("authorization", "").split("Bearer")
        if x.strip()
    ]

    if not (token := (splitted[0] if splitted else None)):
        raise ErrAPI(msg="jwt_not_provided", status=401)

    return token


def check_jwt_mdw(req: Request, optional: bool = False) -> PayloadT | None:

    try:
        token = extract_jwt(req)

    except Exception:
        if optional:
            refresh = req.cookies.get("refresh_token", "")

            if REG_JWE.fullmatch(refresh):
                raise

            return None
        raise

    decoded: PayloadT = check_jwt_lib(token)
    return decoded


def check_jwt_search_us_mdw(
    inst: bool = False, optional: bool = False
) -> Callable[[Request], Awaitable[User | UserDcT | None]]:

    async def _check(req: Request) -> User | UserDcT | None:
        decoded: PayloadT | None = check_jwt_mdw(req, optional=optional)

        if optional and not decoded:
            return None

        # ? if is not optional decoding it will raise ErrAPI so i will not get a key Error trying to access from None a property # noqa: E501

        async with db_trx() as trx:
            us: User | None = None

            try:
                us = await get_us_by_id(
                    trx=trx, us_id=cast(PayloadT, decoded)["user_id"]
                )
            except Exception:
                raise ErrAPI(msg="jwt_invalid", status=401)

            if inst:
                return us
            else:
                return cast(UserDcT, us.to_d())

    return _check
