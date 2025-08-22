from fastapi import APIRouter
from src.features.wake_up.controllers.get import wake_up_ctrl


router_wake_up = APIRouter(prefix="/wake_up")


router_wake_up.add_api_route(
    "/",
    wake_up_ctrl,
    methods=["GET"],
)
