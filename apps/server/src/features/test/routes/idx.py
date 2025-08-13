from fastapi import APIRouter
from src.features.test.controllers.get import (
    get_msg_ctrl,
)
from ..controllers.post import (
    post_form_ctrl,
    post_msg_ctrl,
)

router_test = APIRouter(prefix="/test")


router_test.get("/")(get_msg_ctrl)
router_test.post("/")(post_msg_ctrl)
router_test.post("/form")(post_form_ctrl)
