from math import ceil
from fastapi import Depends, Request, Response
from sqlalchemy import BinaryExpression, select
from src.conf.db import db_trx
from src.decorators.res import ResAPI
from src.lib.db.query import build_conditions
from src.middleware.tokens.check_jwt import check_jwt_search_us_mdw
from src.models.job_application import JobApplication
from src.models.user import UserDcT


async def read_job_appl_ctrl(
    req: Request, us: UserDcT = Depends(check_jwt_search_us_mdw())
) -> Response:

    async with db_trx() as trx:

        q = req.state.parsed_q

        page = int(q["page"])
        limit = int(q["limit"])
        offset = page * limit

        stmt = select(JobApplication).where(JobApplication.user_id == us["id"])
        cond: list[BinaryExpression] = []

        keys_query = ["company_name", "position_name"]

        for k in keys_query:
            val: str = q.get(k, "").strip()
            cond += build_conditions(getattr(JobApplication, k), val)

        stmt = stmt.where(*cond)
        res = (
            (await trx.execute(stmt.limit(limit).offset(offset)))
            .scalars()
            .all()
        )

        n_hits = len(res)
        pages = ceil(n_hits / limit)

        return ResAPI(req).ok_200(
            n_hits=n_hits,
            pages=pages,
            job_applications=[itm.to_d() for itm in res],
        )
