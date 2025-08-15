from datetime import datetime, timedelta, timezone

import jwt

from src.decorators.err import ErrAPI

JWT_SECRET = "12345"
ALG = "HS256"


def gen_jwt(data: dict) -> None:
    payload = {**data}
    payload["exp"] = datetime.now(timezone.utc) - timedelta(minutes=15)

    token = jwt.encode(payload, JWT_SECRET, algorithm=ALG)

    print(token)


# gen_jwt({"id": "abcdefg"})


def verify_jwt(token: str) -> None:
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[ALG])

        print(decoded)
    except jwt.ExpiredSignatureError:
        raise ErrAPI(msg="ACCESS_TOKEN_EXPIRED", status=401)
    except jwt.InvalidTokenError:
        raise ErrAPI(msg="ACCESS_TOKEN_INVALID", status=401)
