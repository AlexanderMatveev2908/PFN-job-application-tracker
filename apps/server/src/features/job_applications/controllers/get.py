from fastapi import Depends, Request, Response
from sqlalchemy import UnaryExpression, select
from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.decorators.res import ResAPI
from src.features.job_applications.middleware.get_appl_by_id import (
    GetApplByIdMdwReturnT,
    get_appl_by_id_mdw,
)
from src.features.job_applications.middleware.read_job_appl import (
    read_job_appl_mdw,
)
from src.lib.db.query import (
    ApplyPagReturnT,
    apply_pagination,
    build_order_query,
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

        cond_order: list[UnaryExpression] = build_order_query(
            q,
            Table=JobApplication,
            keys=["created_at_sort", "updated_at_sort", "applied_at_sort"],
        )

        if cond_order:
            stmt = stmt.order_by(*cond_order)

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


async def get_appl_by_id_ctrl(
    req: Request,
    res_check: GetApplByIdMdwReturnT = Depends(get_appl_by_id_mdw),
) -> Response:

    async with db_trx() as trx:
        application = (
            await trx.execute(
                select(JobApplication).where(
                    JobApplication.id == res_check["application_id"]
                )
            )
        ).scalar_one_or_none()

        if not application:
            raise ErrAPI(msg="application not found", status=404)

        return ResAPI(req).ok_200(application=application)
