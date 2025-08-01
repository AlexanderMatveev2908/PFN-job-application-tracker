from pathlib import Path
from fastapi import Request

from src.decorators.res import ResAPI


async def get_test(req: Request) -> ResAPI:

    form = getattr(req.state, "parsed_f", {})

    if vid := form.get("video", None):
        # os.remove(vid["path"])
        pf = Path(vid["path"])
        print(pf.exists())
        pf.unlink(missing_ok=True)

    return ResAPI.ok_200()
