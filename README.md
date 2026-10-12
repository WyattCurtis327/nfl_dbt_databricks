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

The semantic layer uses the latest YAML spec. It needs dbt 1.12 or newer, or dbt v2. `dbt_project.yml` requires `>=1.12.0`. `requirements.txt` and the Databricks job pin `dbt-databricks>=1.12.0,<2.0.0`. There is no top-level `semantic_models` list, no `measures` list, and no `type_params` wrapper.

| What | Where |
|---|---|
| Semantic models, entities, dimensions, and metrics | `models/gold/schema.yml`, on `game_summaries` and `team_performance_by_season` |
| Saved queries | `models/gold/semantic_models.yml` |
| Daily time spine | `metricflow_time_spine` in `models/gold/schema.yml` |

`game_summaries` keeps that name. Its primary entity is `game` on `game_id`. `agg_time_dimension` is `gameday`. The `week` column is the dimension `game_week`, because MetricFlow reserves `week`.

`team_performance_by_season` is published as the semantic model `team_performance`. The primary entity `team_season` and the time dimension `season_start` are under `derived_semantics`, because neither is a single column. `agg_time_dimension` is `season_start`, which is January 1 of that season.

Simple metrics carry `agg` and `expr` on the metric. Ratio metrics (`upset_rate`, `home_cover_rate`, `win_percentage`, `points_per_game`, `points_allowed_per_game`) use `numerator` and `denominator`. The two models do not join. A positive spread means the home team was favored by that many points.

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
