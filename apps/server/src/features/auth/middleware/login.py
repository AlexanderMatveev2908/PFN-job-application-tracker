from fastapi import Request
from src.lib.validators.idx import EmailFormT, PwdFormT
from src.middleware.forms.check_form import check_form_mdw


class LoginForm(EmailFormT, PwdFormT):
    pass


async def login_mdw(req: Request) -> LoginForm:
    data = await check_form_mdw(LoginForm, req)

    return data
