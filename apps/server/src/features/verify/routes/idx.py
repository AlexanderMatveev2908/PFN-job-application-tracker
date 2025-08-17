from fastapi import APIRouter
from src.features.verify.controllers.post import confirm_email_ctrl


verify_router = APIRouter(prefix="/verify")

verify_router.post("/confirm-email")(confirm_email_ctrl)
