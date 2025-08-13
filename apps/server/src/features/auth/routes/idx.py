from fastapi import APIRouter

from src.features.auth.controllers.post import register_ctrl


auth_router = APIRouter(prefix="/auth")

auth_router.post("/register")(register_ctrl)
