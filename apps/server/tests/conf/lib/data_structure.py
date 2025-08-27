import base64
from typing import Any, Literal, cast

import pyotp

from src.__dev_only.payloads import RegisterPayloadT
from src.constants.reg import REG_CBC_HMAC, REG_SECRET_TOTP
from src.decorators.err import ErrAPI
from src.lib.algs.fernet import check_fernet
from src.lib.data_structure import b_to_d, h_to_b
from src.lib.etc import grab
from src.lib.tokens.cbc_hmac import AadT
from src.models.token import TokenT


def extract_login_payload(
    payload_register: RegisterPayloadT,
) -> dict[Literal["email", "password"], str]:
    return {
        "email": payload_register["email"],
        "password": payload_register["password"],
    }


def get_aad_cbc_hmac(token: str, token_t: TokenT) -> AadT:
    assert REG_CBC_HMAC.fullmatch(token)

    parsed: dict = b_to_d(h_to_b(token.split(".")[0]))

    assert TokenT(parsed["token_t"]) == token_t

    return cast(AadT, parsed)


def gen_totp(totp_secret: str) -> str:

    parsed = totp_secret
    try:
        if not REG_SECRET_TOTP.fullmatch(totp_secret):
            raise ErrAPI(
                msg="secret probably encrypted with fernet alg", status=500
            )
        base64.b32decode(totp_secret, casefold=False)

    except Exception:
        print("value was not b32")
        parsed = (check_fernet(h_to_b(totp_secret))).decode()

    return pyotp.TOTP(parsed).now()


def assrt_msg(d: Any, msg: str) -> None:
    assert msg in grab(d, "msg")
