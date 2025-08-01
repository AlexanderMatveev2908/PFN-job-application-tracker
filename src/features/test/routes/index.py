from fastapi import APIRouter


from ..controllers.get import get_test

router_test = APIRouter(prefix="/test")

router_test.add_api_route(
    "/",
    get_test,
    methods=["GET", "POST"],
)
