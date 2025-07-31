from pathlib import Path


script_file = Path(__file__).resolve()
script_dir = script_file.parent

# print(script_file)
# print(script_dir)

app_dir = Path.cwd()


def write_f(relative: str, content: str) -> None:
    joined = app_dir.joinpath(relative)
    joined.parent.mkdir(parents=True, exist_ok=True)

    if not joined.exists():
        joined.touch()

    with open(joined, "w") as f:
        f.write(content)
