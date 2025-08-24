import os  # noqa: F401
from src.lib.TFA.backup import gen_backup_codes
from src.lib.emails.idx import gen_html_template  # noqa: F401
from src.lib.etc import wrap_loop  # noqa: F401

print("script worked ✅")


print(gen_backup_codes())
