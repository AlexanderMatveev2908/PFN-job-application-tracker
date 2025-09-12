from typing import cast
from fastapi import Request
from sqlalchemy import select

from src.conf.db import db_trx
from src.constants.reg import REG_ID
from src.decorators.err import ErrAPI
from src.features.job_applications.middleware.post_job_application_mdw import (
    PostJobApplMdwReturnT,
    post_job_application_mdw,
)
from src.models.job_application import JobApplication, JobApplicationDct


class PutApplicationMdwReturnT(PostJobApplMdwReturnT):
    existing: JobApplicationDct


async def put_application_mdw(req: Request) -> PutApplicationMdwReturnT:
    application_id = req.path_params.get("application_id", "")

    if not REG_ID.fullmatch(application_id):
        raise ErrAPI(msg="invalid application id", status=422)

    async with db_trx() as trx:
        application = (
            await trx.execute(
                select(JobApplication).where(
                    JobApplication.id == application_id
                )
            )
        ).scalar_one_or_none()

        if not application:
            raise ErrAPI(msg="application not found", status=404)

        return {
            **await post_job_application_mdw(req),
            "existing": cast(JobApplicationDct, application.to_d()),
        }
