from fastapi import APIRouter
from src.features.wake_up.routes.index import router_wake_up
from src.features.test.routes.index import router_test

api = APIRouter(prefix="/api/v1")


api.include_router(router_wake_up)
api.include_router(router_test)
