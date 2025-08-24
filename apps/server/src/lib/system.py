from pathlib import Path
from typing import Any


script_file = Path(__file__).resolve()
script_dir = script_file.parent


APP_DIR = Path.cwd()


def read_f(rel: str) -> str:
    joined = APP_DIR / rel
    print(joined)

    with open(joined, "r", encoding="utf-8") as f:
        content = f.read()
        return content


def write_f(relative: str, content: str) -> None:
    joined = APP_DIR.joinpath(relative)
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
