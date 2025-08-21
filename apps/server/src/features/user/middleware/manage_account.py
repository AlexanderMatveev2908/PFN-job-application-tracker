from fastapi import Request
from src.lib.validators.idx import PwdFormT


class ManageAccountForm(PwdFormT):
    pass


async def manage_account(req: Request) -> None:
    pass
