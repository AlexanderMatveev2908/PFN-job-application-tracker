from fastapi import APIRouter
from src.features.test.controllers.get import (
    get_msg_ctrl,
    get_user_ctrl,
)
from ..controllers.post import (
    post_company_ctrl,
    post_form_ctrl,
    post_job_ctrl,
    post_msg_ctrl,
    post_user_ctr,
)

router_test = APIRouter(prefix="/test")

router_test.post("/user")(post_user_ctr)
router_test.get("/user/{user_id}")(get_user_ctrl)
router_test.post("/company")(post_company_ctrl)
router_test.post("/job")(post_job_ctrl)


router_test.get("/")(get_msg_ctrl)
router_test.post("/")(post_msg_ctrl)

router_test.post("/form")(post_form_ctrl)
