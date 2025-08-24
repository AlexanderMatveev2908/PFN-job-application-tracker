import os


def gen_backup_codes() -> list[str]:
    codes = []
    for _ in range(8):
        code = os.urandom(4).hex().upper()
        codes.append(f"{code[:4]}-{code[4:]}")
    return codes
