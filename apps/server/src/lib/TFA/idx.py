from typing import TypedDict
import pyotp


def gen_totp_secret() -> str:
    secret = pyotp.random_base32()

    return secret


class GenTotpNowReturnT(TypedDict):
    code: str
    uri: str | None


def gen_totp_code(
    secret: str, user_email: str | None = None
) -> GenTotpNowReturnT:
    totp = pyotp.TOTP(secret)

    uri: str | None = None

    if user_email:
        uri = totp.provisioning_uri(
            name=user_email, issuer_name="pfn-job-application-tracker"
        )

    return {"code": totp.now(), "uri": uri}


def check_totp(secret: str, user_code_db: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(user_code_db, valid_window=1)
