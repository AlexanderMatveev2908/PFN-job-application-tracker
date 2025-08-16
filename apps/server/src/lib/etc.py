import asyncio
from time import time
from typing import Callable, Coroutine, Literal, TypeVar

from src.decorators.err import ErrAPI

T = TypeVar("T")


def wrap_loop(
    cb: Callable[[], Coroutine[None, None, T]] | Coroutine[None, None, T],
) -> None:
    if asyncio.iscoroutine(cb):
        fn = cb
    else:
        fn = cb()

    try:
        asyncio.get_running_loop()
        asyncio.create_task(fn)
    except RuntimeError:
        asyncio.run(fn)


ParamExpT = Literal["15m", "1d"]


def calc_exp(param: ParamExpT) -> int:
    base = int(time())
    if param == "15m":
        add = 60 * 15
    elif param == "1d":
        add = (60**2) * 24
    else:
        raise ErrAPI(msg="invalid param", status=500)

    return base + add * 100
