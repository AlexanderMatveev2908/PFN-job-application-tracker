import json
from fastapi import Request
from ..lib.system import write_f


async def log_json(
    req: Request,
) -> None:
    body = await req.body()
    parsed = {}

    try:
        parsed = json.loads(body)
    except Exception as err:
        print(err)

    obj = {}

    obj["body"] = parsed
    obj["params"] = dict(req.path_params)
    obj["query"] = dict(req.query_params)

    obj["access_token"] = req.headers.get("authorization", None)
    obj["refresh_token"] = req.cookies.get("refresh_token", None)

    write_f("logger/log.json", json.dumps(obj, indent=2))
