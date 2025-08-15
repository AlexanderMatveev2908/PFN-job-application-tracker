from fastapi import APIRouter, Depends

from src.features.auth.controllers.post import register_ctrl
from src.middleware.rate_limiter import rate_limit


auth_router = APIRouter(prefix="/auth")

auth_router.post(
    "/register",
    dependencies=[
        Depends(
            rate_limit(
                limit=10,
            )
        )
    ],
)(register_ctrl)
