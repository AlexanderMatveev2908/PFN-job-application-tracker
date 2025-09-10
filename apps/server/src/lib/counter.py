import asyncio
from dataclasses import dataclass
import time
from typing import Awaitable, Callable

from src.lib.logger import clg


@dataclass
class AsyncInterval:
    interval: float
    cb: Callable[[], Awaitable[None]]
    id: asyncio.Task | None = None

    async def _loop(self) -> None:
        while True:
            await asyncio.sleep(self.interval)
            await self.cb()

    def start(self) -> None:
        self.id = asyncio.create_task(self._loop())

    def stop(self) -> None:
        if self.id:
            self.id.cancel()


async def counter_cb(cb: Callable[[], Awaitable[None]]) -> None:
    count = 0

    async def inc() -> None:
        nonlocal count
        count += 1

        print(f"⏳ elapsed {count} sec ⏳")

    t0 = time.perf_counter()

    interval = AsyncInterval(interval=1, cb=inc)
    interval.start()

    try:
        await cb()
    except Exception as err:
        clg(err, ttl="err counter")
    finally:
        interval.stop()

        t1 = time.perf_counter() - t0
        print(f"operation last {t1} ms ⏰")
