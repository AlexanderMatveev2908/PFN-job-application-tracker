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

project_table["requires-python"] = ">=3.12,<4.0"

tool_table = doc.setdefault("tool", table())
black_table = tool_table.setdefault("black", table())
black_table["line-length"] = 79
black_table["target-version"] = ["py312"]

conf_p.write_text(dumps(doc))
print("✅ [project] requires-python updated and [tool.black] configured.")
