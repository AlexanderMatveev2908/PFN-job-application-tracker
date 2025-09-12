from typing import Literal, cast
from fastapi import Depends, Request, Response
from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.features.job_applications.middleware.put_application import (
    PutApplicationMdwReturnT,
    put_application_mdw,
)
from src.models.job_application import JobApplication


async def put_application_ctrl(
    req: Request,
    res_check: PutApplicationMdwReturnT = Depends(put_application_mdw),
) -> Response:

    async with db_trx() as trx:

        existing = cast(
            JobApplication,
            await trx.get(
                JobApplication,
                res_check["existing"]["id"],
            ),
        )

        for k in [
            "company_name",
            "position_name",
            "notes",
            "status",
            "applied_at",
        ]:
            setattr(
                existing,
                k,
                res_check["job_appl"][
                    cast(
                        Literal[
                            "company_name",
                            "position_name",
                            "notes",
                            "status",
                            "applied_at",
                        ],
                        k,
                    )
                ],
            )

        await trx.flush([existing])
        await trx.refresh(existing)

        return ResAPI(req).ok_200(job_application=existing.to_d())
