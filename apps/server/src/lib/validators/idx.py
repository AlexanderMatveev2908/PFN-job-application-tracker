from src.constants.reg import REG_PWD
from src.decorators.err import ErrAPI


def validate_password_lib(v: str) -> str:

    if not REG_PWD.match(v):
        raise ErrAPI(
            msg="Password must have at least 1 lowercase, 1 uppercase, "
            "1 number, 1 symbol, and be 8+ chars long",
            status=422,
        )
    return v
