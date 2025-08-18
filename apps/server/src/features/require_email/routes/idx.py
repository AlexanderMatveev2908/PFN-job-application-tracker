from fastapi import APIRouter

from src.features.require_email.controllers.pos import (
    require_email_forgot_pwd_ctrl,
)


require_email_router = APIRouter(prefix="/require-email")


require_email_router.post("/forgot-pwd")(require_email_forgot_pwd_ctrl)
