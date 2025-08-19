from fastapi import APIRouter, Depends
from src.features.verify.controllers.post import (
    confirm_email_ctrl,
    forgot_pwd_ctrl,
)
from src.middleware.rate_limiter import rate_limit_mdw


verify_router = APIRouter(prefix="/verify")

verify_router.get(
    "/confirm-email", dependencies=[Depends(rate_limit_mdw(limit=5))]
)(confirm_email_ctrl)
verify_router.get(
    "/forgot-pwd", dependencies=[Depends(rate_limit_mdw(limit=3))]
)(forgot_pwd_ctrl)
