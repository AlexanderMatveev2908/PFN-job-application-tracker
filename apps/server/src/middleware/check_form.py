import json
from typing import Type, TypeVar
from fastapi import Request
from pydantic import BaseModel, ValidationError
from src.decorators.err import ErrAPI


FormT = TypeVar("FormT", bound=BaseModel)


async def check_form_mdw(model: Type[FormT], req: Request) -> FormT:

    parsed: dict | None = None

    try:
        parsed = json.loads(await req.body())
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
