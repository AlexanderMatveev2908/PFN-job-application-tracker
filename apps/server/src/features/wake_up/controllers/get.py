from fastapi import Request, Response


async def wake_up_ctrl(req: Request, res: Response) -> dict[str, str]:

    return {"msg": "Ops I did not listen the alarm ⏰ "}
