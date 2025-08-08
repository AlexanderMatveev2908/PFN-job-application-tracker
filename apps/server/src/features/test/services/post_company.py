from src.features.test.middleware.check_company import CompanyT
from src.models.company import Company
from src.conf.db import db_trx


async def post_company_svc(company: CompanyT) -> Company:

    async with db_trx() as trx:
        await trx.begin()

        c = Company(**company.model_dump())
        trx.add(c)
        await trx.flush([c])
        await trx.refresh(c)

        return c
