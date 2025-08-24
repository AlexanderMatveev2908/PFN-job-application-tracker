import os  # noqa: F401
from src.lib.TFA.totp import gen_totp_secret
from src.lib.emails.idx import gen_html_template  # noqa: F401
from src.lib.etc import wrap_loop  # noqa: F401

print("script worked ✅")


print(len(gen_totp_secret(user_email="eg@gmail.com")["secret"]))
