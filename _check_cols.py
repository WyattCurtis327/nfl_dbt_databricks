import json
from pathlib import Path

root = Path(__file__).resolve().parent
for rel in ("models/bronze/schema.yml", "models/silver/schema.yml", "models/gold/schema.yml", "models/sources.yml", "models/column_docs.md"):
    text = (root / rel).read_text(encoding="utf-8")
    print(rel, "docs", text.count("doc('col_"), "bytes", len(text))

manifest = json.load(open(root / "target" / "manifest.json", encoding="utf-8"))
print("generated", manifest["metadata"]["generated_at"])
total = empty = 0
for node in list(manifest["nodes"].values()) + list(manifest["sources"].values()):
    if node.get("resource_type") not in ("model", "source"):
        continue
    cols = node.get("columns") or {}
    blank = sum(1 for col in cols.values() if not (col.get("description") or "").strip())
    total += len(cols)
    empty += blank
    print(node["resource_type"], node.get("name"), len(cols), "empty", blank)
print("total", total, "empty", empty)
semantic = json.load(open(root / "target" / "semantic_manifest.json", encoding="utf-8"))
print(
    "semantic",
    len(semantic.get("semantic_models") or []),
    len(semantic.get("metrics") or []),
    len(semantic.get("saved_queries") or []),
)
