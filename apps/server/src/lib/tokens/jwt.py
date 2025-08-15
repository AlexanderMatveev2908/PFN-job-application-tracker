from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from src.conf.env import get_env
from src.decorators.err import ErrAPI

ALG = "HS256"

env_var = get_env()


def gen_jwt(**kwargs: Any) -> str:
    payload = {**kwargs}
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=15)

    token = jwt.encode(payload, env_var.jwt_secret, algorithm=ALG)

    return token


def verify_jwt(token: str) -> str:
    try:
        decoded = jwt.decode(token, env_var.jwt_secret, algorithms=[ALG])

        return decoded
    except jwt.ExpiredSignatureError:
        raise ErrAPI(msg="ACCESS_TOKEN_EXPIRED", status=401)
    except jwt.InvalidTokenError:
        raise ErrAPI(msg="ACCESS_TOKEN_INVALID", status=401)
