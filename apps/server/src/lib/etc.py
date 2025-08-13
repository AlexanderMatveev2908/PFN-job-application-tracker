import asyncio
from typing import Callable, Coroutine, TypeVar

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
