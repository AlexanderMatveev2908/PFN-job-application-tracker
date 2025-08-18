from typing import Literal
from fastapi import Request
from pydantic import Field

from src.lib.validators.idx import EmailForm
from src.middleware.check_form import check_form_mdw

ActRequireEmailT = Literal["FORGOT_PWD", "CONFIRM_EMAIL"]


class RequestEmailForm(EmailForm):
    act: ActRequireEmailT = Field(...)


async def require_email_mdw(req: Request) -> RequestEmailForm:
    data = await check_form_mdw(RequestEmailForm, req)

    return data
