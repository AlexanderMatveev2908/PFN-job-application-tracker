from fastapi import Depends, Request, Response
from sqlalchemy import select
from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.features.job_applications.middleware.read_job_appl import (
    read_job_appl_mdw,
)
from src.lib.db.query import (
    ApplyPagReturnT,
    apply_pagination,
    build_list_cond_query,
)
from src.middleware.forms.check_form import CheckFormLoggedReturnT
from src.models.job_application import JobApplication


async def read_job_appl_ctrl(
    req: Request,
    res_check: CheckFormLoggedReturnT = Depends(read_job_appl_mdw),
) -> Response:

    async with db_trx() as trx:

        q = res_check["data"]

        # ? define root cond • look for user appl only
        stmt = select(JobApplication).where(
            JobApplication.user_id == res_check["us_d"]["id"]
        )

        # ? chain stmt where cond • avoid boilerplate & repetition,
        # ? find pattern and use it
        # ? to chain any kind of text inputs send from client
        stmt = stmt.where(
            *build_list_cond_query(
                query=q,
                Table=JobApplication,
                keys=["company_name", "position_name"],
            )
        )

        status = q.get("status", [])
        if status:
            stmt = stmt.where(JobApplication.status.in_(status))

        # ? count results before final stmt
        # ? to know how many there are before paginating
        res_pag: ApplyPagReturnT = await apply_pagination(trx, stmt, q)

        stmt = res_pag["stmt_paginated"]

        res = (await trx.execute(stmt)).scalars().all()

        return ResAPI(req).ok_200(
            n_hits=res_pag["n_hits"],
            pages=res_pag["pages"],
            job_applications=[itm.to_d() for itm in res],
        )
