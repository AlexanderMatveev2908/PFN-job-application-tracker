from typing import TypedDict
import pyotp

from src.decorators.err import ErrAPI
from src.lib.algs.fernet import check_fernet
from src.lib.data_structure.etc import h_to_b


class GenTotpSecretReturnT(TypedDict):
    secret: str
    uri: str


def gen_totp_secret(user_email: str) -> GenTotpSecretReturnT:
    secret: str = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(
        name=user_email, issuer_name="pfn-job-application-tracker"
    )
    return {"secret": secret, "uri": uri}


def check_totp_lib(secret: str | bytes | None, user_code: str) -> bool:

    if not secret:
        raise ErrAPI(msg="missing user secret", status=409)

    secret_b: bytes = bytes()

    if isinstance(secret, str):
        secret_b = h_to_b(secret)
    else:
        secret_b = secret

    decrypted_secret = check_fernet(encrypted=secret_b)
    secret_b_32 = decrypted_secret.decode()

    totp = pyotp.TOTP(secret_b_32)

    if not totp.verify(user_code, valid_window=1):
        raise ErrAPI(
            msg="totp_code_invalid",
            status=401,
        )

    return True
