from fastapi import APIRouter, Depends

from src.features.auth.controllers.patch import (
    recover_pwd_ctrl,
    revocer_pwd_2FA_ctrl,
)
from src.features.auth.controllers.post import (
    login_2FA_ctrl,
    login_backup_code_ctrl,
    login_ctrl,
    login_totp_ctrl,
    refresh_token_ctrl,
    register_ctrl,
)
from src.middleware.rate_limiter import rate_limit_mdw


auth_router = APIRouter(prefix="/auth")

auth_router.add_api_route(
    "/register",
    register_ctrl,
    methods=["POST"],
    dependencies=[Depends(rate_limit_mdw(limit=10))],
)

auth_router.add_api_route(
    "/login",
    login_ctrl,
    methods=["POST"],
    dependencies=[Depends(rate_limit_mdw(limit=5, window_arg="1h"))],
)

auth_router.add_api_route(
    "/recover-pwd",
    recover_pwd_ctrl,
    methods=["PATCH"],
    dependencies=[Depends(rate_limit_mdw(limit=5))],
)

auth_router.add_api_route(
    "/recover-pwd-2FA",
    revocer_pwd_2FA_ctrl,
    methods=["PATCH"],
    dependencies=[Depends(rate_limit_mdw(limit=5))],
)

auth_router.add_api_route(
    "/login-2FA",
    login_2FA_ctrl,
    methods=["POST"],
    dependencies=[Depends(rate_limit_mdw(limit=5, window_arg="1h"))],
)

# auth_router.add_api_route(
#     "/login-2FA-totp",
#     login_totp_ctrl,
#     methods=["POST"],
#     dependencies=[Depends(rate_limit_mdw(limit=5, window_arg="1h"))],
# )

# auth_router.add_api_route(
#     "/login-2FA-backup-code",
#     login_backup_code_ctrl,
#     methods=["POST"],
#     dependencies=[Depends(rate_limit_mdw(limit=5, window_arg="1h"))],
# )

auth_router.add_api_route(
    "/refresh",
    refresh_token_ctrl,
    methods=["GET"],
)
