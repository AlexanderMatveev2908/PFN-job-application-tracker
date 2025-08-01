import inspect
from pathlib import Path
from datetime import datetime


def clg(
    *arg,
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

    frame = ""
    for fr in inspect.stack():
        filename = fr.filename
        if "src/" in filename and "lib/logger" not in filename:
            frame = fr
            break

    caller_file = Path(frame.filename if frame else "").resolve()
    print(f"📌 => from {caller_file}")

    print("\t")
