from fastapi import Depends, Request

from src.decorators.res import ResAPI
from src.features.require_email.middleware.require_email import (
    RequireEmailForm,
    require_email_mdw,
)


async def require_email_forgot_pwd_ctrl(
    _: Request,
    require_email_data: RequireEmailForm = Depends(require_email_mdw),
) -> ResAPI:

    return ResAPI.ok_200(**require_email_data.model_dump())
