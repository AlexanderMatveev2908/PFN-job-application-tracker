from fastapi import Depends, Request, Response
from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.features.job_applications.middleware.post_put_job_application import (
    post_put_job_application_mdw,
)
from src.middleware.tokens.check_jwt import check_jwt_search_us_mdw
from src.models.job_application import JobApplication
from src.models.user import UserDcT


async def add_job_appl_ctrl(
    req: Request,
    us_d: UserDcT = Depends(check_jwt_search_us_mdw()),
    job_appl_data: dict = Depends(post_put_job_application_mdw),
) -> Response:

    async with db_trx() as trx:

        job_appl = JobApplication(**job_appl_data, user_id=us_d["id"])

        trx.add(job_appl)
        await trx.flush([job_appl])
        await trx.refresh(job_appl)

        return ResAPI(req).ok_200(job_application=job_appl.to_d())
