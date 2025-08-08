from src.conf.db import db_trx
from src.features.test.middleware.check_job import JobT
from src.models.job import Job


async def post_job_svc(job: JobT) -> Job:
    async with db_trx() as trx:
        j = Job(**job.model_dump())

        trx.add(j)
        await trx.flush([j])
        await trx.refresh(j)

        return j
