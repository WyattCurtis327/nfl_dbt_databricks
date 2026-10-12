# NFL

dbt project for the NFL medallion on Databricks, plus a MetricFlow semantic layer on the gold marts.

| | |
|---|---|
| dbt project | `nfl` |
| Profile | `nfl` in `~/.dbt/profiles.yml` |
| Workspace | `https://dbc-89a97ed5-5f7d.cloud.databricks.com` |
| CLI profile | `wyatts_databricks` |
| Warehouse | Serverless Starter Warehouse (`abae422499df211c`) |
| Catalog | `nfl` |

Bronze, silver, and gold tables are written in the `nfl` catalog. Sources are the tables already in `nfl.landing`. This project does not reload them.

The full click-by-click setup and both deploy paths are in [docs/setup-and-deployment.md](docs/setup-and-deployment.md).

## Layers

| Layer | Relation | What it is |
|---|---|---|
| Landing | `nfl.landing.*` | Source tables. Not built by dbt. |
| Bronze | `nfl.bronze.games`, `teams`, `players`, `game_odds`, `roster_weeks` | Landing rows plus `_ingest_timestamp`, `_source_schema`, and `_source_table`. |
| Silver | same five names | Dates cast, players without an id dropped, scores and team names cleaned. |
| Gold | `game_summaries`, `team_performance_by_season`, `metricflow_time_spine` | One row per game with the closing line, one row per team season, and the daily date spine MetricFlow needs. |

Model files are prefixed (`bronze_games`) so dbt names stay unique. The table name is the `alias`.

## Semantic layer

`models/gold/semantic_models.yml` defines MetricFlow semantic models, metrics, and saved queries on `game_summaries` and `team_performance_by_season`. The two models do not join. A positive spread means the home team was favored by that many points.

Query those metrics by name only after a dbt platform deploy job has published the semantic manifest. `dbt build` on Databricks materializes the tables. It does not turn on the Semantic Layer API. See the deployment doc.

`nfl.gold.game_pick_metrics` is a Unity Catalog metric view from another pipeline. This project does not replace it.

## Run locally

```powershell
$env:DATABRICKS_CONFIG_PROFILE = "wyatts_databricks"
if ($env:DATABRICKS_HOST -and $env:DATABRICKS_HOST -notlike "http*") {
  $env:DATABRICKS_HOST = "https://$($env:DATABRICKS_HOST)"
}
.\.venv\Scripts\Activate.ps1
dbt deps
dbt build
```

OAuth uses the Databricks CLI login for `wyatts_databricks`. No token is stored in the profile. Re-run `databricks auth login --host https://dbc-89a97ed5-5f7d.cloud.databricks.com --profile wyatts_databricks` if that login expires.
