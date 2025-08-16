import asyncio
import json
from fastapi import Depends, Request
from src.decorators.res import ResAPI
from src.features.auth.middleware.register import register_mdw
from src.features.test.services.register import register_flow_test_ctrl
from src.lib.s3.post import upload_w3
from src.lib.system import del_vid


async def post_form_ctrl(req: Request) -> ResAPI:

    parsed_f = req.state.parsed_f

    images = parsed_f["images"]

    uploaded_images = await asyncio.gather(*(upload_w3(img) for img in images))

    uploaded_video = await upload_w3(parsed_f["video"])

    del_vid(parsed_f)

    return ResAPI.ok_201(
        uploaded_images=uploaded_images, uploaded_video=uploaded_video
    )


async def post_msg_ctrl(req: Request) -> ResAPI:

    b = (json.loads(await req.body())).get("msg", None)

    if isinstance(b, str) and len(b.strip()):
        return ResAPI.ok_200(msg="✅ msg received ☎️")

    return ResAPI.ok_200()


async def post_tokens_ctrl(req: Request, user=Depends(register_mdw)) -> ResAPI:

    res = await register_flow_test_ctrl(user)

    return ResAPI.ok_200(res=res)
