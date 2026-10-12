import json

m = json.load(open(r"target/manifest.json", encoding="utf-8"))
bad = []
for node in list(m["nodes"].values()) + list(m["sources"].values()):
    if node.get("resource_type") not in ("model", "source"):
        continue
    for name, meta in (node.get("columns") or {}).items():
        d = meta.get("description") or ""
        flags = []
        if "\n" in d or "\r" in d:
            flags.append("nl")
        if "'" in d:
            flags.append("quote")
        if "`" in d:
            flags.append("tick")
        if len(d) > 900:
            flags.append("long")
        if flags:
            bad.append((node["name"], name, ",".join(flags), d[:160]))
print("bad", len(bad))
for row in bad:
    print(row)
