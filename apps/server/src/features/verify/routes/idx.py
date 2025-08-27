from fastapi import APIRouter, Depends
from src.features.verify.controllers.get import (
    confirm_email_ctrl,
    confirm_new_email_ctrl,
    forgot_pwd_ctrl,
)
from src.features.verify.controllers.patch import (
    confirm_new_email_2FA_backup_code_ctrl,
    confirm_new_email_2FA_top_ctrl,
)
from src.features.verify.controllers.post import (
    forgot_pwd_2FA_backup_code_ctrl,
    forgot_pwd_2FA_totp_ctrl,
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
    "/recover-pwd",
    forgot_pwd_ctrl,
    methods=["GET"],
    dependencies=[Depends(rate_limit_mdw(limit=3))],
)

verify_router.add_api_route(
    "/recover-pwd-2FA-totp",
    forgot_pwd_2FA_totp_ctrl,
    methods=["POST"],
    dependencies=[Depends(rate_limit_mdw(limit=3))],
)

verify_router.add_api_route(
    "/recover-pwd-2FA-backup-code",
    forgot_pwd_2FA_backup_code_ctrl,
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
    "/new-email-2FA-totp",
    confirm_new_email_2FA_top_ctrl,
    methods=["PATCH"],
    dependencies=[Depends(rate_limit_mdw(limit=5))],
)

verify_router.add_api_route(
    "/new-email-2FA-backup-code",
    confirm_new_email_2FA_backup_code_ctrl,
    methods=["PATCH"],
    dependencies=[Depends(rate_limit_mdw(limit=5))],
)
