from fastapi import Depends, Request, Response
from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.features.job_applications.middleware.post_job_application_mdw import (
    PostJobApplMdwReturnT,
    post_job_application_mdw,
)
from src.models.job_application import JobApplication


async def add_job_appl_ctrl(
    req: Request,
    res_check: PostJobApplMdwReturnT = Depends(post_job_application_mdw),
) -> Response:

    async with db_trx() as trx:

        job_appl = JobApplication(**res_check["job_appl"])

        trx.add(job_appl)
        await trx.flush([job_appl])
        await trx.refresh(job_appl)

        return ResAPI(req).ok_201(job_application=job_appl.to_d())
