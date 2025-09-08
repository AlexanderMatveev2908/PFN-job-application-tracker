import json
from typing import Awaitable, Callable, Generic, Type, TypedDict, cast
from fastapi import Request
from pydantic import ValidationError
from src.decorators.err import ErrAPI
from src.middleware.tokens.check_jwt import check_jwt_search_us_mdw
from src.models.user import UserDcT
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


class CheckFormLoggedReturnT(TypedDict, Generic[FormT]):
    form_inst: FormT
    us_d: UserDcT


def check_form_mdw_logged(
    model: Type[FormT],
    data: dict | None = None,
) -> Callable[[Request], Awaitable[CheckFormLoggedReturnT]]:

    async def _check(req: Request) -> CheckFormLoggedReturnT:
        us_d = cast(UserDcT, await check_jwt_search_us_mdw()(req))

        params_check: dict = {"model": model}
        if data:
            params_check["data"] = data
        else:
            params_check["req"] = req

        return {
            "form_inst": await check_form_mdw(**params_check),
            "us_d": us_d,
        }

    return _check
