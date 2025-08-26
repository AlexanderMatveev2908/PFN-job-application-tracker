import asyncio
import json
from time import time
from typing import Any, Callable, Coroutine, Literal, TypeVar

from fastapi import Request

from src.decorators.err import ErrAPI
from src.my_types.idx import MAPPER_WINDOW_TIME, ParamWindowTime

T = TypeVar("T")


def wrap_loop(
    cb: Callable[[], Coroutine[None, None, T]] | Coroutine[None, None, T],
) -> None:
    if asyncio.iscoroutine(cb):
        fn = cb
    else:
        fn = cb()

    try:
        loop = asyncio.get_running_loop()
        loop.create_task(fn)
    except RuntimeError:
        asyncio.run(fn)


FormatCalcExpT = Literal["ms", "sec"]


def calc_exp(
    param: ParamWindowTime,
    reverse: bool = False,
    format: FormatCalcExpT = "ms",
) -> int:
    base = int(time())

    add = MAPPER_WINDOW_TIME.get(param)
    if not add:
        raise ErrAPI(msg="invalid param", status=500)

    return (base + (-add if reverse else add)) * (
        1000 if format == "ms" else 1
    )


def lt_now(v: int) -> bool:
    return v < time() * 1000


async def parse_bd(req: Request) -> dict:
    return json.loads(await req.body())


def get_now() -> int:
    return int(time() * 1000)


def grab(
    d: Any,
    key: str,
    parent: str | None = None,
    was_under: bool = False,
) -> Any | None:
    for k, v in d.items():

        is_under = was_under or (k == parent)

        if k == key and (parent is None or is_under):
            return v

        if isinstance(v, dict):
            found = grab(v, key, parent, is_under)
            if found is not None:
                return found
    return None
