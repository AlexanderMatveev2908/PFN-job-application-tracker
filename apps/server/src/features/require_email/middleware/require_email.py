from fastapi import Request
from src.lib.validators.idx import EmailForm
from src.middleware.check_form import check_form_mdw


class RequireEmailForm(EmailForm):
    pass


async def require_email_mdw(req: Request) -> RequireEmailForm:
    data = await check_form_mdw(RequireEmailForm, req)

    return data
