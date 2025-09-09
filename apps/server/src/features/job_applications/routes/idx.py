from fastapi import APIRouter, Depends

from src.features.job_applications.controllers.get import read_job_appl_ctrl
from src.features.job_applications.controllers.post import add_job_appl_ctrl
from src.middleware.security.rate_limiter import rate_limit_mdw


job_applications_router = APIRouter(prefix="/job-applications")


job_applications_router.add_api_route(
    "/",
    add_job_appl_ctrl,
    methods=["POST"],
    dependencies=[Depends(rate_limit_mdw(20))],
)

job_applications_router.add_api_route("/", read_job_appl_ctrl, methods=["GET"])
