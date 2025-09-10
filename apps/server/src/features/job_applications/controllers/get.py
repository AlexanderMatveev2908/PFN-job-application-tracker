from fastapi import Depends, Request, Response
from sqlalchemy import select
from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.lib.db.query import (
    ApplyPagReturnT,
    apply_pagination,
    build_list_cond_query,
)
from src.middleware.tokens.check_jwt import check_jwt_search_us_mdw
from src.models.job_application import JobApplication
from src.models.user import UserDcT


async def read_job_appl_ctrl(
    req: Request, us: UserDcT = Depends(check_jwt_search_us_mdw())
) -> Response:

    async with db_trx() as trx:

        q = req.state.parsed_q

        # ? define root cond • look for user appl only
        stmt = select(JobApplication).where(JobApplication.user_id == us["id"])

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
