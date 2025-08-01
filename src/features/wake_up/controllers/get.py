import json
from fastapi import Request, Response


async def wake_up_ctrl(req: Request, res: Response) -> dict[str, str]:
    b = await req.body()
    p = b.decode()
    s = json.loads(p)
    print(s)

    return {"msg": "Pps I did not listen the alarm ⏰ "}
