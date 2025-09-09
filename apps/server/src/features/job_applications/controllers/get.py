from math import ceil
from fastapi import Depends, Request, Response
from sqlalchemy import select
from src.conf.db import db_trx
from src.decorators.res import ResAPI
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

        company_name: str = q.get("company_name", "").strip()
        position_name: str = q.get("position_name", "").strip()

        company_words: list[str] = [w for w in company_name.split() if w]
        position_words: list[str] = [w for w in position_name.split() if w]

        stmt = select(JobApplication).where(JobApplication.user_id == us["id"])

        for w in company_words:
            stmt = stmt.where(JobApplication.company_name.ilike(f"%{w}%"))

        for w in position_words:
            stmt = stmt.where(JobApplication.position_name.ilike(f"%{w}%"))

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
