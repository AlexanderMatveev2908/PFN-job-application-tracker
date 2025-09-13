from typing import cast
from fastapi import Request
from sqlalchemy import select

from src.conf.db import db_trx
from src.decorators.err import ErrAPI
from src.lib.validators.idx import check_id_lib
from src.middleware.tokens.check_jwt import check_jwt_search_us_mdw
from src.models.job_application import JobApplication, JobApplicationDct
from src.models.user import UserDcT
from src.my_types.idx import UserDctReturnT


class DelApplMdwReturnT(UserDctReturnT):
    existing: JobApplicationDct


async def del_appl_mdw(req: Request) -> DelApplMdwReturnT:
    application_id = check_id_lib(req, "application_id")

    us_d = cast(UserDcT, await check_jwt_search_us_mdw()(req))

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
            "us_d": us_d,
            "existing": cast(JobApplicationDct, application.to_d()),
        }
