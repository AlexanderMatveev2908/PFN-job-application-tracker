from fastapi import Request
from pydantic import UUID4, BaseModel, Field

from src.middleware.check_form import check_form_mdw


class JobT(BaseModel):
    title: str = Field(..., max_length=50)
    user_id: UUID4 = Field(
        ...,
    )
    company_id: UUID4 = Field(
        ...,
    )


async def check_job_mdw(req: Request) -> JobT:
    data = check_form_mdw(JobT, await req.body())

    return data
