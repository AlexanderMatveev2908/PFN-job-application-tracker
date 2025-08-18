from fastapi import APIRouter, Depends

from src.features.auth.controllers.post import login_ctrl, register_ctrl
from src.middleware.rate_limiter import rate_limit_mdw


auth_router = APIRouter(prefix="/auth")

auth_router.post(
    "/register",
    dependencies=[
        Depends(
            rate_limit_mdw(
                limit=10,
            )
        )
    ],
)(register_ctrl)
auth_router.post(
    "/login", dependencies=[Depends(rate_limit_mdw(limit=5, window_arg="1h"))]
)(login_ctrl)
