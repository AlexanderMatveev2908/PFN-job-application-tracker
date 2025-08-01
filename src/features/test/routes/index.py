from fastapi import APIRouter

from src.middleware.wrap_api import wrap_api
from ..controllers.get import get_test

router_test = APIRouter(prefix="/test")

router_test.add_api_route(
    "/",
    wrap_api(get_test),
    methods=["GET"],
)
