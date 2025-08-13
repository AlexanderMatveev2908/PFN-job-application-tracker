from fastapi import APIRouter

from src.features.auth.controllers.post import register_ctrl


authRouter = APIRouter(prefix="/auth")

authRouter.post("/register")(register_ctrl)
