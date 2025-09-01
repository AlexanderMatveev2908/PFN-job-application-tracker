from typing import TypedDict

from src.__dev_only.payloads import RegisterPartPayloadT
from src.models.user import UserDcT


class LoginOkReturnT(TypedDict):
    access_token: str
    refresh_token: str


class RegisterOkLibReturnT(LoginOkReturnT):
    payload: RegisterPartPayloadT


class SuccessReqTokensReturnT(RegisterOkLibReturnT):
    user: UserDcT
    cbc_hmac_token: str


class User2FAReturnT(SuccessReqTokensReturnT):
    totp_secret: str
    backup_codes: list[str]
