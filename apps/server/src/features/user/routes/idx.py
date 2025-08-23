from fastapi import APIRouter, Depends

from src.features.user.controllers.delete import delete_account_ctrl
from src.features.user.controllers.patch import (
    change_email_ctrl,
    change_pwd_ctrl,
)
from src.features.user.controllers.post import (
    get_access_account_ctrl,
)
from src.middleware.rate_limiter import rate_limit_mdw


user_router = APIRouter(prefix="/user")

user_router.add_api_route(
    "/manage-account",
    get_access_account_ctrl,
    methods=["POST"],
    dependencies=[Depends(rate_limit_mdw(limit=5))],
)

user_router.add_api_route(
    "/change-pwd",
    change_pwd_ctrl,
    methods=["PATCH"],
    dependencies=[Depends(rate_limit_mdw(limit=10))],
)

user_router.add_api_route(
    "/change-email",
    change_email_ctrl,
    methods=["PATCH"],
    dependencies=[Depends(rate_limit_mdw(10))],
)

user_router.add_api_route(
    "/delete-account",
    delete_account_ctrl,
    methods=["DELETE"],
    dependencies=[Depends(rate_limit_mdw(limit=5))],
)
