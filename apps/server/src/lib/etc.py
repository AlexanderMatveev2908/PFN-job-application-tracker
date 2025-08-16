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


ParamExpT = Literal["15m", "1h", "1d"]

mp: dict[ParamExpT, int] = {
    "15m": 15 * 60,
    "1h": 60**2,
    "1d": 24 * 60**2,
}


def calc_exp(param: ParamExpT, reverse: bool = False) -> int:
    base = int(time())

    add = mp.get(param)
    if add is None:
        raise ErrAPI(msg="invalid param", status=500)

    return (base + (-add if reverse else add)) * 1000
