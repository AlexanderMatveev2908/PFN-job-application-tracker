import datetime
from typing import TypedDict, cast
from fastapi import Request
from pydantic import BaseModel, Field

from src.constants.reg import REG_DATE_PICKER, REG_NAME, REG_TXT
from src.middleware.forms.check_form import (
    check_form_mdw_logged,
)
from src.models.job_application import ApplicationStatusT, JobApplicationDct
from src.models.user import UserDcT


class JobApplicationFormT(BaseModel):
    company_name: str = Field(
        min_length=1, max_length=100, pattern=REG_NAME.pattern
    )

    position_name: str = Field(
        min_length=1, max_length=100, pattern=REG_NAME.pattern
    )

    date_applied: str = Field(min_length=1, pattern=REG_DATE_PICKER.pattern)

    status: ApplicationStatusT

    notes: str | None = Field(
        default=None, max_length=1000, pattern=REG_TXT.pattern
    )


class PostPutJobApplMdwReturnT(TypedDict):
    job_appl: JobApplicationDct
    us_d: UserDcT


async def post_put_job_application_mdw(
    req: Request,
) -> PostPutJobApplMdwReturnT:

    res_check = await check_form_mdw_logged(
        JobApplicationFormT, data=getattr(req.state, "parsed_f", None)
    )(req)

    return {
        "job_appl": cast(
            JobApplicationDct,
            {
                **res_check["form_inst"].model_dump(),
                "date_applied": int(
                    datetime.datetime.fromisoformat(
                        res_check["form_inst"].date_applied
                    )
                    .replace(tzinfo=datetime.timezone.utc)
                    .timestamp()
                    * 1000
                ),
                "user_id": res_check["us_d"]["id"],
            },
        ),
        "us_d": res_check["us_d"],
    }
