import asyncio
import json
from fastapi import Depends, Request
from src.decorators.res import ResAPI
from src.features.test.middleware.check_company import (
    CompanyT,
    check_company_mdw,
)
from src.features.test.middleware.check_job import JobT, check_job_mdw
from src.features.test.middleware.check_user import UserT, check_user_mdw
from src.features.test.services.post_company import post_company_svc
from src.features.test.services.post_job import post_job_svc
from src.features.test.services.post_user import post_user_svc
from src.lib.logger import clg
from src.lib.s3.post import upload_w3
from src.lib.system import del_vid


async def post_user_ctr(
    _: Request, user: UserT = Depends(check_user_mdw)
) -> ResAPI:

    us = await post_user_svc(user)

    return ResAPI.ok_201(us=us.to_d())


async def post_company_ctrl(
    _: Request, company: CompanyT = Depends(check_company_mdw)
) -> ResAPI:

    c = await post_company_svc(company)

    return ResAPI.ok_200(c=c.to_d())


async def post_job_ctrl(
    _: Request, job: JobT = Depends(check_job_mdw)
) -> ResAPI:

    j = await post_job_svc(job)

    return ResAPI.ok_200(j=j.to_d())


async def post_form_ctrl(req: Request) -> ResAPI:

    parsed_f = req.state.parsed_f

    images = parsed_f["images"]

    uploaded_images = await asyncio.gather(*(upload_w3(img) for img in images))

    clg(uploaded_images)
    uploaded_video = await upload_w3(parsed_f["video"])

    del_vid(parsed_f)

    return ResAPI.ok_201(
        uploaded_images=uploaded_images, uploaded_video=uploaded_video
    )


async def post_msg_ctrl(req: Request) -> ResAPI:

    b = (json.loads(await req.body())).get("msg", None)

    if isinstance(b, str) and len(b.strip()):
        return ResAPI.ok_200(msg="✅ msg received ☎️")

    return ResAPI.err_400()
