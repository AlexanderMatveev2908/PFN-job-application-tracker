import uuid
import jwt

from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.lib.data_structure.parsers import parse_id
from src.lib.etc import calc_exp
from src.models.token import PayloadT

ALG = "HS256"

env_var = get_env()


def gen_jwt(user_id: str | uuid.UUID, reverse: bool = False) -> str:

    parsed_id: str = parse_id(user_id)
    payload: dict[str, str | int] = {"user_id": parsed_id}
    payload["exp"] = calc_exp(
        "60s" if env_var.py_env != "test" else "15m",
        reverse=reverse,
        format="sec",
    )

    token: str = jwt.encode(payload, env_var.jwt_secret, algorithm=ALG)

    return token


def check_jwt_lib(token: str, dirty: bool = False) -> PayloadT:
    try:
        decoded: PayloadT = jwt.decode(
            token + ("👻 some random text for fun" if dirty else ""),
            env_var.jwt_secret,
            algorithms=[ALG],
        )

        return decoded
    except jwt.ExpiredSignatureError:
        raise ErrAPI(msg="jwt_expired", status=401)
    except jwt.InvalidTokenError:
        raise ErrAPI(msg="jwt_invalid", status=401)
