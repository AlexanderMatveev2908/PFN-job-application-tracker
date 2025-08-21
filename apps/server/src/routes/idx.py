from fastapi import APIRouter
from src.features.wake_up.routes.idx import router_wake_up
from src.features.test.routes.idx import router_test
from src.features.auth.routes.idx import auth_router
from src.features.verify.routes.idx import verify_router
from src.features.require_email.routes.idx import require_email_router
from src.features.user.routes.idx import user_router

api = APIRouter(prefix="/api/v1")

api.include_router(router_wake_up)
api.include_router(router_test)
api.include_router(auth_router)
api.include_router(verify_router)
api.include_router(require_email_router)
api.include_router(user_router)
