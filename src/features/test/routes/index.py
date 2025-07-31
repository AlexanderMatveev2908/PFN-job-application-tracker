from fastapi import APIRouter, Depends

from src.middleware.log_json import log_json
from ..controllers.get import get_test

router_test = APIRouter(prefix="/test")

router_test.add_api_route(
    "/", get_test, methods=["GET"], dependencies=[Depends(log_json)]
)
