from src.conf.env import get_env
from src.decorators.res import ClearCookieT, CookieT


mode = get_env().py_env


def gen_refresh_cookie(refresh_token: str) -> CookieT:
    return {
        "key": "refresh_token",
        "value": refresh_token,
        "httponly": True,
        "secure": mode != "test",
        "samesite": "lax" if mode == "test" else "none",
        "max_age": 60**2,
        "path": "/",
    }


def gen_clear_refresh_token() -> ClearCookieT:
    return {
        "key": "refresh_token",
        "path": "/",
    }
