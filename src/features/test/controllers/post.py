import asyncio
from fastapi import Depends, Request
from src.conf.s3 import upload_w3
from src.decorators.res import ResAPI
from src.features.test.middleware.check_user import User, check_user
from src.lib.logger import clg
from src.lib.system import del_vid


async def post_test(_: Request, user: User = Depends(check_user)) -> ResAPI:

    return ResAPI.ok_201(data=user)


async def post_form(req: Request) -> ResAPI:

    parsed_f = req.state.parsed_f
    del_vid(parsed_f)

    images = parsed_f["images"]

    result = await asyncio.gather(*(upload_w3(img) for img in images))

    clg(result, ttl="aws images")

    return ResAPI.ok_201(result=result)
