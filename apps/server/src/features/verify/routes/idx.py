from fastapi import APIRouter, Depends
from src.features.verify.controllers.get import (
    confirm_email_ctrl,
    forgot_pwd_ctrl,
)
from src.middleware.rate_limiter import rate_limit_mdw


verify_router = APIRouter(prefix="/verify")

verify_router.add_api_route(
    "/confirm-email",
    confirm_email_ctrl,
    methods=["GET"],
    dependencies=[Depends(rate_limit_mdw(limit=5))],
)

verify_router.add_api_route(
    "/forgot-pwd",
    forgot_pwd_ctrl,
    methods=["GET"],
    dependencies=[Depends(rate_limit_mdw(limit=3))],
)
