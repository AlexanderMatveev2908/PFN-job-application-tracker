from fastapi import APIRouter, Depends

from src.features.user.controllers.post import get_access_account_ctrl
from src.middleware.rate_limiter import rate_limit_mdw


user_router = APIRouter(prefix="/user")

user_router.post(
    "/manage-account", dependencies=[Depends(rate_limit_mdw(limit=5))]
)(get_access_account_ctrl)
