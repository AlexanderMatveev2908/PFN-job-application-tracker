from pathlib import Path
from tomlkit import parse, dumps, document, table, inline_table

conf_p = Path("pyproject.toml")

# ? Load or create pyproject.toml
if not conf_p.exists():
    doc = document()
else:
    doc = parse(conf_p.read_text())

# ? Project section
project_table = doc.get("project") or table()
doc["project"] = project_table
project_table["requires-python"] = ">=3.12,<4.0"

# ? Tool section
tool_table = doc.get("tool") or table()
doc["tool"] = tool_table

# ? Black formatter
black_table = tool_table.get("black") or table()
tool_table["black"] = black_table
black_table.setdefault("line-length", 79)
black_table.setdefault("target-version", ["py312"])

# ? Ruff linter
ruff_table = tool_table.get("ruff") or table()
tool_table["ruff"] = ruff_table
ruff_table.setdefault("line-length", 79)

lint_table = ruff_table.get("lint") or table()
ruff_table["lint"] = lint_table

legacy_ignore = ruff_table.get("ignore")
current_ignore = set(lint_table.get("ignore", []))
if legacy_ignore:
    current_ignore.update(legacy_ignore)
    ruff_table.pop("ignore", None)
current_ignore.update({"E203", "E741"})
lint_table["ignore"] = sorted(current_ignore)

# ? MyPy type checker
mypy_table = tool_table.get("mypy") or table()
tool_table["mypy"] = mypy_table
mypy_defaults = {
    "python_version": "3.12",
    "mypy_path": ["src"],
    "ignore_missing_imports": True,
    "disallow_untyped_defs": True,
    "no_implicit_optional": True,
    "warn_unused_ignores": True,
    "show_error_codes": True,
    "plugins": ["sqlalchemy.ext.mypy.plugin"],
}
for k, v in mypy_defaults.items():
    mypy_table.setdefault(k, v)

# ? Poetry packaging
poetry_table = tool_table.get("poetry") or table()
tool_table["poetry"] = poetry_table
if poetry_table.get("packages") is None:
    pkg = inline_table()
    pkg["include"] = "src"
    pkg["from"] = "."
    poetry_table["packages"] = [pkg]

# ? Include HTML templates in package
include_list = poetry_table.get("include") or []
if not any(
    isinstance(item, dict) and item.get("path") == "src/lib/emails/*.html"
    for item in include_list
):
    html_entry = inline_table()
    html_entry["path"] = "src/lib/emails/*.html"
    include_list.append(html_entry)
poetry_table["include"] = include_list

# ? Pytest config
pytest_table = tool_table.get("pytest") or table()
tool_table["pytest"] = pytest_table
ini = pytest_table.get("ini_options") or table()
pytest_table["ini_options"] = ini
ini.setdefault("testpaths", ["tests"])
ini.setdefault("python_files", ["test_*.py", "*_test.py"])
ini.setdefault("python_functions", ["*_t", "test_*"])
ini.setdefault("python_classes", ["*TST", "Test*"])
ini["addopts"] = (
    "-v --no-header --json-report --json-report-file=test-results/reports.json"
)
ini.setdefault("asyncio_mode", "strict")
ini.setdefault("pythonpath", [".", "apps/server"])

# ? Save file
conf_p.write_text(dumps(doc))
print("✅ pyproject.toml updated")
