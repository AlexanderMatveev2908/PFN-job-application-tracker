import datetime
from fastapi import Request
from pydantic import BaseModel, Field

from src.constants.reg import REG_DATE_PICKER, REG_NAME, REG_TXT
from src.middleware.forms.check_form import check_form_mdw
from src.models.job_application import ApplicationStatusT


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


async def post_put_job_application_mdw(req: Request) -> dict:
    data = await check_form_mdw(JobApplicationFormT, data=req.state.parsed_f)

    return {
        **data.model_dump(),
        "date_applied": int(
            datetime.datetime.fromisoformat(data.date_applied)
            .replace(tzinfo=datetime.timezone.utc)
            .timestamp()
            * 1000
        ),
    }
