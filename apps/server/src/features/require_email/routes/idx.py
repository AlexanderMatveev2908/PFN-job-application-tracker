from fastapi import APIRouter, Depends
from src.features.require_email.controllers.post import (
    confirm_email_ctrl,
    require_email_forgot_pwd_ctrl,
)
from src.middleware.rate_limiter import rate_limit_mdw


require_email_router = APIRouter(prefix="/require-email")

require_email_router.add_api_route(
    "/forgot-pwd",
    require_email_forgot_pwd_ctrl,
    methods=["POST"],
    dependencies=[Depends(rate_limit_mdw(limit=3))],
)

require_email_router.add_api_route(
    "/confirm-email",
    confirm_email_ctrl,
    methods=["POST"],
    dependencies=[Depends(rate_limit_mdw(limit=5))],
)
