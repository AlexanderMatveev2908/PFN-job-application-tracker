from fastapi import APIRouter, Depends
from src.features.test.controllers.get import (
    get_msg_ctrl,
    get_protected_data_ctrl,
)
from src.middleware.security.rate_limiter import rate_limit_mdw
from ..controllers.post import (
    get_err_ctrl,
    get_us_2FA_ctrl,
    post_form_ctrl,
    post_msg_ctrl,
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
    dependencies=[Depends(rate_limit_mdw(limit=10))],
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

router_test.add_api_route("/get-user-2FA", get_us_2FA_ctrl, methods=["POST"])

router_test.add_api_route(
    "/get-err",
    get_err_ctrl,
    methods=["POST"],
)

router_test.add_api_route(
    "/protected",
    get_protected_data_ctrl,
    methods=["GET"],
)
