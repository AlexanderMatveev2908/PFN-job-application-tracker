import re
import regex

REG_NAME = regex.compile(r"^[\p{L}\s`']*$", flags=regex.UNICODE)

REG_PWD = regex.compile(
    rf"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])\S{8,}$",  # noqa: E231
    flags=regex.UNICODE,
)

REG_TXT = regex.compile(r"^[\p{L}\d\s\-\'\",;!?]*$", flags=regex.UNICODE)

REG_INT = re.compile(r"^\d+$")

REG_FLOAT = re.compile(r"(^\d+(\.\d{1,2})?$)|(^\.\d{1,2}$)")

REG_ID = re.compile(
    r"^([a-f0-9]{8})-([a-f0-9]{4})-4[a-f0-9]{3}-([a-f0-9]{4})-([a-f0-9]{12})$"
)
