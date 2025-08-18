from fastapi import Request

from src.lib.validators.idx import EmailForm


class RequestEmailForm(EmailForm):
    pass


async def require_email_mdw(req: Request) -> None:
    pass
