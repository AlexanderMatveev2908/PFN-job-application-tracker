from pathlib import Path
from typing import Any


script_file = Path(__file__).resolve()
script_dir = script_file.parent


app_dir = Path.cwd()


def write_f(relative: str, content: str) -> None:
    joined = app_dir.joinpath(relative)
    joined.parent.mkdir(parents=True, exist_ok=True)

    if not joined.exists():
        joined.touch()

    with open(joined, "w") as f:
        f.write(content)


def del_vid(form: dict[str, Any]) -> None:
    if vid := form.get("video", None):
        # os.remove(vid["path"])
        pf = Path(vid["path"])
        pf.unlink(missing_ok=True)
