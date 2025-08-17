import jwt

from src.conf.env import get_env
from src.decorators.err import ErrAPI
from src.lib.etc import calc_exp
from src.models.token import PayloadT

ALG = "HS256"

env_var = get_env()


def gen_jwt(arg: PayloadT, reverse: bool = False) -> str:
    payload = {**arg}
    payload["exp"] = calc_exp("15m", reverse=reverse, format="sec")

    token = jwt.encode(payload, env_var.jwt_secret, algorithm=ALG)

    return token


def verify_jwt(token: str, dirty: bool = False) -> str:
    try:
        decoded = jwt.decode(
            token + ("👻 some random text for fun" if dirty else ""),
            env_var.jwt_secret,
            algorithms=[ALG],
        )

        return decoded
    except jwt.ExpiredSignatureError:
        raise ErrAPI(msg="ACCESS_TOKEN_EXPIRED", status=401)
    except jwt.InvalidTokenError:
        raise ErrAPI(msg="ACCESS_TOKEN_INVALID", status=401)
