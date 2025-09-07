import json
from typing import Type
from fastapi import Request
from pydantic import ValidationError
from src.decorators.err import ErrAPI
from src.my_types.idx import FormT


async def check_form_mdw(
    model: Type[FormT],
    req: Request | None = None,
    data: dict | None = None,
) -> FormT:

    parsed: dict | None = None

    try:
        if isinstance(req, Request):
            parsed = json.loads(await req.body())
        elif isinstance(data, dict):
            parsed = data
    except Exception:
        pass

    if parsed is None:
        raise ErrAPI(msg="wrong data format", status=422)

    try:

        instance = model(**parsed)
        return instance
    except ValidationError as err:
        arg_errs = err.errors()

        raise ErrAPI(
            msg=f'{arg_errs[0]["loc"][0]} => {arg_errs[0]["msg"]}',
            status=422,
            list_errs=arg_errs,
        )
