import inspect
from pathlib import Path
from datetime import datetime
from typing import Any, Optional


def cent(txt: str, t: bool = True) -> None:
    l: int = len(txt)

    print(txt.center(l + 4, " ").center(l + 20, "—"))

    if t:
        print("\t")


def clg(
    *arg: Any | list[Any],
    ttl: str = "logger",
) -> None:

    print(
        f"{(f'{ttl} 🔥'.center(len(ttl) + 4, ' ')).center(len(ttl) + 20, '—')}"
    )

    if len(arg):
        print("\t")
        for x in arg:
            print(x)

    print("\t")

    now = datetime.now()
    time_parsed = f'⏰ => at {now.strftime("%H:%M:%S")}'
    print(time_parsed)

    frame: Optional[inspect.FrameInfo] = None
    for fr in inspect.stack():
        filename = fr.filename
        if "src/" in filename and "lib/logger" not in filename:
            frame = fr
            break

    caller_file = Path(frame.filename if frame else "").resolve()
    print(f"📌 => from {caller_file}")

    print("\t")
