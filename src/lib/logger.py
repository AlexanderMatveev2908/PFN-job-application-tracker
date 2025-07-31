import inspect
from pathlib import Path
from datetime import datetime


def __cg(
    *arg,
    ttl: str = "logger",
) -> None:

    print(
        f"{(f'{ttl} 🔥'.center(len(ttl) + 4, ' ')).center(len(ttl) * 4, '—')}"
    )

    caller_file = Path(inspect.stack()[1].filename).resolve()

    for x in arg:
        print(x)

    now = datetime.now()
    time_parsed = f'⏰ => {now.strftime("%H:%M:%S")}'
    print(time_parsed)

    print(f"📌 => from {caller_file}")
