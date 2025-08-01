import re

import regex


REG_TXT = regex.compile(r"^[\p{L}\d\s\-\'\",;!?]*$", flags=regex.UNICODE)

REG_INT = re.compile(r"^\d+$")
REG_FLOAT = re.compile(r"(^\d+(\.\d{1,2})?$)|(^\.\d{1,2}$)")
REG_ID = re.compile(
    r"^([a-f0-9]{8})-([a-f0-9]{4})-4[a-f0-9]{3}-([a-f0-9]{4})-([a-f0-9]{12})$"
)
