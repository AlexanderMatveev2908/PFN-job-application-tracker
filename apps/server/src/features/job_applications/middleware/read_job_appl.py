from fastapi import Request
from pydantic import Field
from src.constants.reg import REG_JOB_NAME
from src.lib.validators.idx import PaginationFormT
from src.middleware.forms.check_form import (
    CheckFormLoggedReturnT,
    check_form_mdw_logged,
)
from src.models.job_application import ApplicationStatusT


class ReadJobsFormT(PaginationFormT):
    company_name: str | None = Field(
        max_length=100, pattern=REG_JOB_NAME.pattern, default=None
    )

    position_name: str | None = Field(
        max_length=100, pattern=REG_JOB_NAME.pattern, default=None
    )

    status: list[ApplicationStatusT] | None = Field(default=None)


async def read_job_appl_mdw(req: Request) -> CheckFormLoggedReturnT:

    data = await check_form_mdw_logged(
        data=getattr(req.state, "parsed_q"), model=ReadJobsFormT
    )(req)

    return {"us_d": data["us_d"], "data": data["data"]}
