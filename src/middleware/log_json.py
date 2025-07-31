import json
from fastapi import Request


async def log_json(
    req: Request,
) -> None:
    body = await req.body()
    parsed = {}

    try:
        parsed = json.loads(body)
    except Exception as err:
        print(err)

    print(parsed)
