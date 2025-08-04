from pathlib import Path
from tomlkit import parse, dumps, document, table

conf_p = Path("pyproject.toml")

if not conf_p.exists():
    print("📄 No pyproject.toml found, creating new one...")
    doc = document()
    project_table = table()
    doc["project"] = project_table
else:
    print("📄 Found existing pyproject.toml, updating...")
    doc = parse(conf_p.read_text())
    project_table = doc.setdefault("project", table())

# [project]
project_table["requires-python"] = ">=3.12,<4.0"

# [tool.black]
tool_table = doc.setdefault("tool", table())
black_table = tool_table.setdefault("black", table())
black_table.setdefault("line-length", 79)
black_table.setdefault("target-version", ["py312"])

# [tool.mypy]
mypy_table = tool_table.setdefault("mypy", table())

defaults = {
    "python_version": "3.12",
    "mypy_path": ["src"],
    "ignore_missing_imports": True,
    "disallow_untyped_defs": True,
    "no_implicit_optional": True,
    "warn_unused_ignores": True,
    "show_error_codes": True,
    "plugins": ["sqlalchemy.ext.mypy.plugin"],
}

for k, v in defaults.items():
    mypy_table.setdefault(k, v)

conf_p.write_text(dumps(doc))
print("✅ Updated [project], [tool.black], and [tool.mypy].")
