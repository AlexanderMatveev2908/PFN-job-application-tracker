from fastapi import Depends, Request, Response
from sqlalchemy import delete

from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.job_applications.middleware.del_appl import (
    DelApplMdwReturnT,
    del_appl_mdw,
)
from src.models.job_application import JobApplication


async def del_appl_ctrl(
    req: Request, res_check: DelApplMdwReturnT = Depends(del_appl_mdw)
) -> Response:

    async with db_trx() as trx:
        res_del = await trx.execute(
            delete(JobApplication).where(
                JobApplication.id == res_check["existing"]["id"]
            )
        )

        if res_del.rowcount != 1:
            raise ErrAPI(msg="application not found", status=404)

        return ResAPI(req).ok_200(msg="application deleted")
