import asyncio
from typing import Awaitable, Callable


def wrap_async(cb: Callable | Awaitable) -> None:
    if asyncio.iscoroutine(cb):
        fn = cb
    else:
        fn = cb()  # type: ignore

    try:
        asyncio.get_running_loop()
        asyncio.create_task(fn)
    except RuntimeError:
        asyncio.run(fn)
