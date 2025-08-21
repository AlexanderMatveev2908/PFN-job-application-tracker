from fastapi import Request
from src.lib.validators.idx import EmailForm, PwdFormT
from src.middleware.check_form import check_form_mdw


class LoginForm(EmailForm, PwdFormT):
    pass


async def login_mdw(req: Request) -> LoginForm:
    data = await check_form_mdw(LoginForm, req)

    return data
