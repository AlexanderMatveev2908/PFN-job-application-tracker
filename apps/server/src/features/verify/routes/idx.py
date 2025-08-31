from fastapi import APIRouter, Depends
from src.features.verify.controllers.get import (
    confirm_email_ctrl,
    confirm_new_email_ctrl,
    forgot_pwd_ctrl,
)
from src.features.verify.controllers.patch import (
    confirm_new_email_2FA_ctrl,
)
from src.features.verify.controllers.post import (
    recover_pwd_2FA_ctrl,
)
from src.middleware.security.rate_limiter import rate_limit_mdw


verify_router = APIRouter(prefix="/verify")

verify_router.add_api_route(
    "/confirm-email",
    confirm_email_ctrl,
    methods=["GET"],
    dependencies=[Depends(rate_limit_mdw(limit=5))],
)

verify_router.add_api_route(
    "/recover-pwd",
    forgot_pwd_ctrl,
    methods=["GET"],
    dependencies=[Depends(rate_limit_mdw(limit=3))],
)

verify_router.add_api_route(
    "/recover-pwd-2FA",
    recover_pwd_2FA_ctrl,
    methods=["POST"],
    dependencies=[Depends(rate_limit_mdw(limit=3))],
)

verify_router.add_api_route(
    "/new-email",
    confirm_new_email_ctrl,
    methods=["GET"],
    dependencies=[Depends(rate_limit_mdw(limit=5))],
)

verify_router.add_api_route(
    "/new-email-2FA",
    confirm_new_email_2FA_ctrl,
    methods=["PATCH"],
    dependencies=[Depends(rate_limit_mdw(limit=5))],
)
