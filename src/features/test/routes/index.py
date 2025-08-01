from fastapi import APIRouter

from src.features.test.controllers.get import get_test


from ..controllers.post import post_test

router_test = APIRouter(prefix="/test")

router_test.add_api_route(
    "/",
    post_test,
    methods=["POST"],
)

router_test.add_api_route("/", get_test, methods=["GET"])
