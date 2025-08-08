from fastapi import Request
from pydantic import BaseModel, Field

from src.middleware.check_form import check_form_mdw


class CompanyT(BaseModel):
    name: str = Field(..., max_length=50)


async def check_company_mdw(req: Request) -> CompanyT:
    data = check_form_mdw(CompanyT, await req.body())

    return data
