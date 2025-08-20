import inspect
from pathlib import Path
from datetime import datetime
import traceback
from typing import Any, Optional


def center_txt(txt: str, emoji: str = "") -> str:
    l: int = len(txt)

    raw = f"{emoji} {txt} {emoji}" if emoji else txt

    return raw.center(l + 4, " ").center(l + 20, "—")


def cent(txt: str, t: bool = True) -> None:

    print(center_txt(txt))

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


def log_err(err: Exception) -> None:
    frames = traceback.extract_tb(err.__traceback__)
    src_frames = []

    for f in frames:
        if "src/" in f.filename:
            src_frames.append(
                f"📂 {f.filename} => 🔢 {f.lineno}"
                f" | 🆎 {f.name} | ☢️ {f.line}"
            )

    msg = str(err) or repr(err)
    exc_type = type(err).__name__
    exc_mod = type(err).__module__
    depth = len(frames)
    last = frames[-1]

    print("\t")

    clg(
        *src_frames,
        "\t",
        f"📝 msg => {msg}",
        f"📏 depth => {depth}",
        f"💥 last file => 📁 {last.filename}",
        f" 📏 last line =>  {last.lineno}",
        f" 👻 last def name => {last.name}",
        f" ✏️ last code line =>   {last.line}",
        "\t",
        center_txt("args", emoji="⚠️"),
        repr(err.args),
        "\t",
        center_txt("cause", emoji="⚠️"),
        repr(err.__cause__) if err.__cause__ else None,
        "\t",
        center_txt("context", emoji="⚠️"),
        repr(err.__context__) if err.__context__ else None,
        "\t",
        ttl=f"💣 {exc_type} — {exc_mod}",
    )
