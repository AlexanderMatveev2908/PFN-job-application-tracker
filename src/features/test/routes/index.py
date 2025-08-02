from fastapi import APIRouter

from src.features.test.controllers.get import get_test


from ..controllers.post import post_form, post_test

router_test = APIRouter(prefix="/test")

router_test.add_api_route(
    "/",
    post_test,
    methods=["POST"],
)

router_test.add_api_route("/", get_test, methods=["GET"])

router_test.add_api_route("/form", post_form, methods=["POST"])
