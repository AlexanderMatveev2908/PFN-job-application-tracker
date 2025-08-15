import json
from typing import Any, Type, TypeVar
from pydantic import BaseModel, ValidationError
from src.decorators.err import ErrAPI
from src.lib.logger import clg

FormT = TypeVar("FormT", bound=BaseModel)


def check_form_mdw(model: Type[FormT], data: dict[str, Any] | bytes) -> FormT:

    parsed: dict | None = None

    try:
        if isinstance(data, dict):
            parsed = data

        else:
            parsed = json.loads(bytes(data))
    except Exception as err:
        clg(err, ttl="err parse body")

    if parsed is None:
        raise ErrAPI(msg="Provided wrong data", status=422)

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
