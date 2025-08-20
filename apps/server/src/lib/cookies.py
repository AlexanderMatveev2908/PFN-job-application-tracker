from src.conf.env import get_env
from src.decorators.res import CookieD


mode = get_env().py_env


def gen_refresh_cookie(refresh_token: str) -> CookieD:
    return {
        "key": "refresh_token",
        "value": refresh_token,
        "httponly": True,
        "secure": mode != "test",
        "samesite": "lax" if mode == "test" else "none",
        "max_age": 60**2,
        "path": "/",
    }
