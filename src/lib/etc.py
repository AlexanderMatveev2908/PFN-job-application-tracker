import asyncio
from typing import Callable


def wrap_async(cb: Callable) -> None:
    try:
        asyncio.get_running_loop()
        asyncio.create_task(cb())
    except RuntimeError:
        asyncio.run(cb())
