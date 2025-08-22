from fastapi import APIRouter, Depends
from src.features.test.controllers.get import (
    get_msg_ctrl,
    get_protected_data_ctrl,
)
from src.middleware.rate_limiter import rate_limit_mdw
from ..controllers.post import (
    get_err_ctrl,
    post_form_ctrl,
    post_msg_ctrl,
    tokens_expired_ctrl,
    tokens_health_ctrl,
)

router_test = APIRouter(prefix="/test")

router_test.add_api_route(
    "/",
    get_msg_ctrl,
    methods=["GET"],
)

router_test.add_api_route(
    "/",
    post_msg_ctrl,
    methods=["POST"],
)

router_test.add_api_route(
    "/form",
    post_form_ctrl,
    methods=["POST"],
)

router_test.add_api_route(
    "/tokens-health",
    tokens_health_ctrl,
    methods=["POST"],
)

router_test.add_api_route(
    "/get-tokens-expired",
    tokens_expired_ctrl,
    methods=["POST"],
)

router_test.add_api_route(
    "/get-err-expired",
    get_err_ctrl,
    methods=["POST"],
)

router_test.add_api_route(
    "/get-err-invalid",
    get_err_ctrl,
    methods=["POST"],
)

router_test.add_api_route(
    "/protected",
    get_protected_data_ctrl,
    methods=["GET"],
    dependencies=[Depends(rate_limit_mdw(limit=5))],
)
