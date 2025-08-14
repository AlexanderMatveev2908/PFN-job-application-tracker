from fastapi import APIRouter, Depends
from src.features.test.controllers.get import (
    get_msg_ctrl,
)
from src.middleware.rate_limiter import rate_limit
from ..controllers.post import (
    post_form_ctrl,
    post_msg_ctrl,
)

router_test = APIRouter(prefix="/test")


router_test.get("/", dependencies=[Depends(rate_limit())])(get_msg_ctrl)
router_test.post("/")(post_msg_ctrl)
router_test.post("/form")(post_form_ctrl)
