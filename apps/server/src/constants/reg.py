import re
import regex

REG_NAME = regex.compile(r"^[\p{L}\s`']*$", flags=regex.UNICODE)

REG_PWD = regex.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])\S{8,}$",  # noqa: E231
    flags=regex.UNICODE,
)

REG_TXT = regex.compile(r"^[\p{L}\d\s\-\'\",;!?]*$", flags=regex.UNICODE)

REG_INT = re.compile(r"^\d+$")

REG_FLOAT = re.compile(r"(^\d+(\.\d{1,2})?$)|(^\.\d{1,2}$)")

REG_ID = re.compile(
    r"^([a-f0-9]{8})-([a-f0-9]{4})-4[a-f0-9]{3}-([a-f0-9]{4})-([a-f0-9]{12})$"
)

REG_JWE = re.compile(r"^[A-Fa-f0-9]{1004}$")

REG_CBC_HMAC = re.compile(
    r"^(?=.{600,}$)[A-Fa-f0-9]{400,}\.[A-Fa-f0-9]{32}\.[A-Fa-f0-9]{128}\.[A-Fa-f0-9]{64}$"  # noqa: E501
)

REG_JWT = re.compile(
    r"^(?=.{171}$)[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$"
)

REG_SECRET_TOTP = re.compile(r"^[A-Z2-7]{32}$")

REG_TOTP_CODE = re.compile(r"^\d{6}$")

REG_BACKUP_CODE = re.compile(r"^[A-Z0-9]{4}-[A-Z0-9]{4}$")
