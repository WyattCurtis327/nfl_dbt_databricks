"""Apply rendered dbt column descriptions to Unity Catalog. Not part of the project."""
import json
import os
import subprocess
import sys

MANIFEST = r"c:\Users\wyatt\grok\dbt_demo2\target\manifest.json"
BATCH = 12


def quote(text: str) -> str:
    return text.replace("'", "''")


def main() -> int:
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    statements = []

    def add(relation: str, columns: dict) -> None:
        for name, meta in columns.items():
            desc = (meta.get("description") or "").strip()
            if not desc:
                raise SystemExit(f"missing description for {relation}.{name}")
            statements.append(
                f"ALTER TABLE {relation} ALTER COLUMN `{name}` COMMENT '{quote(desc)}'"
            )

    for node in manifest["nodes"].values():
        if node["resource_type"] != "model":
            continue
        relation = f"{node['database']}.{node['schema']}.{node['alias']}"
        add(relation, node["columns"])
        if node["alias"] == "roster_weeks" and node["schema"] == "bronze":
            add("nfl.bronze.rosters", node["columns"])

    for source in manifest["sources"].values():
        relation = f"{source['database']}.{source['schema']}.{source['name']}"
        add(relation, source["columns"])

    print(f"statements {len(statements)}", flush=True)
    env = os.environ.copy()
    env["DATABRICKS_CONFIG_PROFILE"] = "wyatts_databricks"
    host = env.get("DATABRICKS_HOST") or ""
    if host and not host.startswith("http"):
        env["DATABRICKS_HOST"] = "https://" + host

    failed = []
    for start in range(0, len(statements), BATCH):
        batch = statements[start : start + BATCH]
        cmd = [
            "databricks",
            "experimental",
            "aitools",
            "tools",
            "query",
            "--output",
            "json",
            "-w",
            "abae422499df211c",
            "-p",
            "wyatts_databricks",
            *batch,
        ]
        completed = subprocess.run(cmd, capture_output=True, text=True, env=env)
        if completed.returncode != 0:
            failed.append((start, completed.returncode, completed.stdout[-1500:], completed.stderr[-1500:]))
            print(f"FAIL batch {start} code {completed.returncode}", flush=True)
            print(completed.stderr[-800:], flush=True)
            print(completed.stdout[-800:], flush=True)
            break
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = [{"state": "UNKNOWN", "raw": completed.stdout[:300]}]
        bad = [item for item in payload if item.get("state") not in (None, "SUCCEEDED", "CLOSED")]
        # no-result alters may omit state and just succeed as a list of objects
        if isinstance(payload, list):
            for item in payload:
                state = item.get("state")
                if state and state != "SUCCEEDED":
                    bad.append(item)
        if bad:
            failed.append((start, bad))
            print(f"FAIL batch {start} states", flush=True)
            print(json.dumps(bad)[:1500], flush=True)
            break
        print(f"ok {start + len(batch)}/{len(statements)}", flush=True)

    print("FAILED" if failed else "DONE", len(failed), flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
