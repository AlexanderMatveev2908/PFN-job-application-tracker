from typing import TypedDict
import pyotp


class GenTotpSecretReturnT(TypedDict):
    secret: str
    uri: str


def gen_totp_secret(user_email: str) -> GenTotpSecretReturnT:
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(
        name=user_email, issuer_name="pfn-job-application-tracker"
    )
    return {"secret": secret, "uri": uri}


def check_totp(secret: str, user_code: str) -> bool:

    totp = pyotp.TOTP(secret)
    return totp.verify(user_code, valid_window=1)
