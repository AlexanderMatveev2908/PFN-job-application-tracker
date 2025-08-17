from fastapi import APIRouter
from src.features.test.controllers.get import (
    get_msg_ctrl,
)
from ..controllers.post import (
    get_err_ctrl,
    post_form_ctrl,
    post_msg_ctrl,
    tokens_expired_ctrl,
    tokens_health_ctrl,
)

router_test = APIRouter(prefix="/test")


router_test.get(
    "/",
)(get_msg_ctrl)
router_test.post("/")(post_msg_ctrl)
router_test.post("/form")(post_form_ctrl)

router_test.post("/tokens-health")(tokens_health_ctrl)
router_test.post("/tokens-expired")(tokens_expired_ctrl)
router_test.post("/get-err-expired")(get_err_ctrl)
router_test.post("/get-err-invalid")(get_err_ctrl)
