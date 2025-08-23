from pathlib import Path
from tomlkit import parse, dumps, document, table, inline_table

conf_p = Path("pyproject.toml")

if not conf_p.exists():
    print("📄 No pyproject.toml found, creating new one...")
    doc = document()
else:
    print("📄 Found existing pyproject.toml, updating...")
    doc = parse(conf_p.read_text())

project_table = doc.get("project")
if project_table is None:
    project_table = table()
    doc["project"] = project_table
project_table["requires-python"] = ">=3.12,<4.0"

tool_table = doc.get("tool")
if tool_table is None:
    tool_table = table()
    doc["tool"] = tool_table

black_table = tool_table.get("black")
if black_table is None:
    black_table = table()
    tool_table["black"] = black_table
black_table["line-length"] = black_table.get("line-length", 79)
black_table["target-version"] = black_table.get("target-version", ["py312"])


ruff_table = tool_table.get("ruff")
if ruff_table is None:
    ruff_table = table()
    tool_table["ruff"] = ruff_table

ruff_table["line-length"] = ruff_table.get("line-length", 79)

lint_table = ruff_table.get("lint")
if lint_table is None:
    lint_table = table()
    ruff_table["lint"] = lint_table

legacy_ignore = ruff_table.get("ignore")
current_ignore = set(lint_table.get("ignore", []))

if legacy_ignore:
    current_ignore.update(legacy_ignore)
    try:
        del ruff_table["ignore"]
    except Exception:
        pass

current_ignore.update({"E203", "E741"})
lint_table["ignore"] = sorted(current_ignore)

mypy_table = tool_table.get("mypy")
if mypy_table is None:
    mypy_table = table()
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
for key, default in mypy_defaults.items():
    if mypy_table.get(key) is None:
        mypy_table[key] = default

poetry_table = tool_table.get("poetry")
if poetry_table is None:
    poetry_table = table()
    tool_table["poetry"] = poetry_table

if poetry_table.get("packages") is None:
    pkg = inline_table()
    pkg["include"] = "src"
    pkg["from"] = "."
    poetry_table["packages"] = [pkg]


pytest_table = tool_table.get("pytest")
if pytest_table is None:
    pytest_table = table()
    tool_table["pytest"] = pytest_table

ini = pytest_table.get("ini_options")
if ini is None:
    ini = table()
    pytest_table["ini_options"] = ini

ini["testpaths"] = ["tests"]
ini["python_files"] = ini.get("python_files", ["test_*.py", "*_test.py"])
ini["python_functions"] = ini.get("python_functions", ["*_t", "test_*"])
ini["python_classes"] = ini.get("python_classes", ["*TST", "Test*"])
ini["addopts"] = (
    "-v --no-header --json-report --json-report-file=test-results/reports.json"
)
ini["asyncio_mode"] = ini.get("asyncio_mode", "strict")
ini["pythonpath"] = ini.get("pythonpath", [".", "apps/server"])

conf_p.write_text(dumps(doc))
print("✅ updated pyproject.toml")
