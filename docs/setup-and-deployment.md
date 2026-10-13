# NFL dbt project: setup and deployment

This is the setup that matches this repo and the accounts already on this machine.

| Item | Value |
|---|---|
| dbt project name | `nfl` |
| dbt profile name | `nfl` |
| Databricks user | `wyatt_curtis@hotmail.com` |
| Databricks CLI profile | `wyatts_databricks` (the only valid profile) |
| Workspace | `https://dbc-89a97ed5-5f7d.cloud.databricks.com` |
| SQL warehouse | Serverless Starter Warehouse |
| Warehouse id | `abae422499df211c` |
| HTTP path | `/sql/1.0/warehouses/abae422499df211c` |
| Catalog | `nfl` |
| Source schema | `nfl.landing` |
| Target schemas | `nfl.bronze`, `nfl.silver`, `nfl.gold` |

Two different dbt programs show up in the steps below. They are not interchangeable.

| Program | What it is | Used for |
|---|---|---|
| `dbt-databricks` in `.venv` | dbt Core 1.12 or newer, plus the Databricks adapter | `dbt build` on your laptop and the Databricks job |
| dbt v2, installed by the VS Code extension | The current dbt engine from dbt Labs | Editor features, and the dbt platform account after you sign in |

`pip install dbt` now installs dbt v2, not dbt Core. This repo pins `dbt-databricks>=1.12.0,<2.0.0` in `requirements.txt` and in `resources/nfl.job.yml`. That floor is the first Core release that parses the semantic YAML in this repo. The upper bound keeps the laptop and the Databricks job on Core rather than v2.

The Databricks connection is already logged in. The Cloud CLI config for project NFL is `C:\Users\wyatt\.dbt\dbt_cloud.yml`. Do not commit that file. The VS Code extension keeps its own login; that step is [section 4](#4-sign-in-to-your-dbt-account). The platform project already exists. [Section 7](#7-deploy-the-semantic-layer-on-your-dbt-account) is how this folder gets deployed into it.

## 1. Confirm the Databricks account

Databricks CLI v1.10 is already installed. The valid profile is `wyatts_databricks`. The other profiles (`prod`, `prod-476a24c0`, `prod-1b8eedfc`) point at the same workspace and are not valid. Do not use them.

```powershell
databricks --version
databricks auth profiles
databricks current-user me --profile wyatts_databricks
```

If `wyatts_databricks` is no longer valid, log in again. This opens a browser as `wyatt_curtis@hotmail.com`.

```powershell
databricks auth login --host https://dbc-89a97ed5-5f7d.cloud.databricks.com --profile wyatts_databricks
```

The catalog `nfl` and the schemas `landing`, `bronze`, `silver`, and `gold` already exist. Do not create a second catalog. The Serverless Starter Warehouse already exists. Do not create a second warehouse.

Landing tables this project reads:

- `nfl.landing.games`
- `nfl.landing.teams`
- `nfl.landing.players`
- `nfl.landing.game_odds`
- `nfl.landing.rosters`

## 2. Install the local dbt adapter

From this folder (`c:\Users\wyatt\grok\nfl_dbt_databricks`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
dbt --version
```

`dbt --version` should report dbt Core 1.12 or newer and `databricks` under plugins. The semantic YAML in this repo does not parse on older 1.x releases. If PowerShell blocks the activate script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Local profile

`~/.dbt/profiles.yml` already has a profile named `nfl`. It uses OAuth against the Databricks CLI. It does not store a token.

```yaml
nfl:
  target: dev
  outputs:
    dev:
      type: databricks
      catalog: nfl
      schema: default
      host: dbc-89a97ed5-5f7d.cloud.databricks.com
      http_path: /sql/1.0/warehouses/abae422499df211c
      auth_type: oauth
      threads: 4
```

`schema: default` is only the fallback. `macros/generate_schema_name.sql` writes bronze, silver, and gold models straight into `nfl.bronze`, `nfl.silver`, and `nfl.gold`. It does not prefix those names with `default_`.

Point the shell at the CLI profile before any dbt command. If `DATABRICKS_HOST` is set without `https://`, OAuth fails, so the second line fixes that.

```powershell
$env:DATABRICKS_CONFIG_PROFILE = "wyatts_databricks"
if ($env:DATABRICKS_HOST -and $env:DATABRICKS_HOST -notlike "http*") {
  $env:DATABRICKS_HOST = "https://$($env:DATABRICKS_HOST)"
}
dbt debug
```

`dbt debug` must end with `All checks passed`. The warehouse can be stopped. The first query starts it.

## 4. Sign in to your dbt account

The dbt platform (formerly dbt Cloud) is a separate login from Databricks. The Cloud CLI config for project NFL is already `C:\Users\wyatt\.dbt\dbt_cloud.yml`. Do not commit it, and do not copy the token into this repo. The VS Code extension does not read that file. Sign in there if the status bar does not already show project `nfl`.

1. Install Visual Studio Code if it is not installed: [https://code.visualstudio.com](https://code.visualstudio.com).
2. Open this folder: **File → Open Folder** → `c:\Users\wyatt\grok\nfl_dbt_databricks`.
3. Install the recommended extensions when VS Code prompts, or install them yourself:
   - `dbt` from publisher **dbt Labs, LLC** (extension id `dbtLabsInc.dbt`). This is the only extension dbt Labs supports.
   - `Python` from Microsoft (`ms-python.python`).
4. Command Palette (`Ctrl+Shift+P`) → **Python: Select Interpreter** → `.\.venv\Scripts\python.exe`.
5. Command Palette → **dbt: Sign in** (the label can also be **dbt: Login**). The extension installs dbt v2 if it is missing, then opens a browser.
6. Sign in with the dbt account you already have. Do not create a second account. If the browser offers a region, use the region that account already lives in (often `us1`, which is `https://us1.dbt.com` or `https://cloud.getdbt.com`).
7. Click **Allow access**.
8. The status bar should show **dbt Extension**. Hover it. It should name this project (`nfl`) and a dbt v2 binary. That binary is not `.venv\Scripts\dbt.exe`. Leave it that way.

You can do the same sign-in from a terminal after dbt v2 is on your PATH:

```powershell
dbt login
```

If the venv is active, `dbt` is dbt Core, and `dbt login` will not exist. Open a terminal that is not using `.venv`, or call the v2 binary the extension installed. Editor features use v2. `dbt build` in this repo uses the venv.

## 5. What the project contains

```text
dbt_project.yml                  project name nfl, profile nfl, dbt >=1.12
packages.yml                     no packages
models/sources.yml               nfl.landing
models/bronze/                   landing copy plus audit columns
models/silver/                   types, filters, scores
models/gold/schema.yml           semantic models and metrics on the gold marts
models/gold/semantic_models.yml  saved queries only
macros/generate_schema_name.sql
tests/                           singular tests
dbt_profiles/profiles.yml        Databricks job only
databricks.yml                   bundle
resources/nfl.job.yml            one dbt task, no schedule, dbt-databricks >=1.12
```

A negative `spread_line` means the home team was favored by that many points.

`nfl.bronze.rosters` is a materialized view from another pipeline. This project writes `nfl.bronze.roster_weeks` and does not replace `rosters`.

`nfl.gold.game_pick_metrics` is a Unity Catalog metric view. It is not the dbt Semantic Layer. Leave it alone.

### Semantic layer YAML

This repo uses the latest Semantic Layer spec (dbt 1.12+ and dbt v2). Do not add a top-level `semantic_models` list, a `measures` list, or a `type_params` block. dbt 1.12 also rejects describing the same model in two YAML files, so the semantic config lives on the model and the saved queries live in their own file.

| What | Where |
|---|---|
| Semantic model, columns, entities, dimensions, metrics | `models/gold/schema.yml` |
| Saved queries `games_by_season`, `games_by_week`, `team_seasons` | `models/gold/semantic_models.yml` |
| Time spine | `metricflow_time_spine` in `models/gold/schema.yml` |

`game_summaries` is both the model name and the semantic model name. The primary entity `game` is the `game_id` column. `agg_time_dimension` is `gameday`, with `granularity: day` on that column. Categorical dimensions are the columns `season`, `game_type`, `home_team`, `away_team`, `over_under_result`, `is_upset`, and `beat_spread`. The `week` column is exposed as the dimension `game_week`. MetricFlow reserves the name `week`.

`team_performance_by_season` is published as the semantic model `team_performance`. `season` and `team` are categorical dimensions on those columns. The primary entity `team_season` and the time dimension `season_start` are under `derived_semantics`, because each is an expression rather than one column:

- `team_season` is `concat(cast(season as string), '_', team)`.
- `season_start` is `make_date(cast(season as int), 1, 1)` at year granularity. `agg_time_dimension` points at `season_start`, so team-season `metric_time` is January 1 of that season. A January playoff game on `game_summaries` still falls in the next calendar year, because that model's `metric_time` is `gameday`.

Simple metrics replace measures. `agg` and `expr` are keys on the metric. Ratio metrics use `numerator` and `denominator` directly. The ratios are `upset_rate`, `home_cover_rate`, `win_percentage`, `points_per_game`, and `points_allowed_per_game`. The two semantic models do not join: a game has two teams, so `game` and `team_season` are not the same entity.

`dbt parse` writes `target/semantic_manifest.json`. On dbt 1.12.5 that file has 2 semantic models (`game_summaries`, `team_performance`), 21 metrics, and 3 saved queries. Publishing that manifest to the Semantic Layer API is section 7, not a local `dbt build`.

## 6. Build on Databricks from VS Code or the terminal

From an activated `.venv`, with the profile env vars from section 3:

```powershell
dbt deps
dbt build
```

`dbt deps` does nothing useful today (`packages.yml` is empty). It is here so the command matches the Databricks job in section 8. The dbt platform job in section 7.4 runs `dbt build` only.

`dbt build` runs models and tests. It replaces:

- `nfl.bronze.games`, `teams`, `players`, `game_odds`, `roster_weeks`
- `nfl.silver.games`, `teams`, `players`, `game_odds`, `roster_weeks`
- `nfl.gold.game_summaries`, `team_performance_by_season`, `metricflow_time_spine`

In VS Code, with the dbt extension signed in, you can also right-click a model and run **Build** or **Preview**. Preview uses the extension's dbt v2 engine and the same `nfl` profile.

Check the semantic layer parses:

```powershell
dbt parse
```

After a successful parse, `target/semantic_manifest.json` exists. Expect 2 semantic models, 21 metrics, and 3 saved queries. That file is local. Downstream tools cannot query it until a dbt platform deploy job publishes it (section 7).

Useful narrower commands:

```powershell
dbt build --select gold
dbt test --select team_performance_by_season
dbt show --select game_summaries --limit 20
```

## 7. Deploy the semantic layer on your dbt account

The Semantic Layer API runs only in a dbt platform **deployment** environment. A laptop `dbt build` and a Databricks job do not publish it.

You need a dbt platform plan that includes the Semantic Layer (Starter, Enterprise, or Enterprise+, including a Starter trial). Developer querying against the Semantic Layer is not available yet. Queries hit the deployment environment.

### 7.1 Connect this Git repo

dbt platform deploys from a Git repo. This folder is already one. Do not run `git init` again.

| | |
|---|---|
| Branch | `main` |
| Origin | `https://github.com/WyattCurtis327/nfl_dbt_databricks.git` |

The NFL project on dbt platform is linked to this repo. Platform jobs build `main`.

### 7.2 The platform project

Account `wyatts_dbt` (`https://ib010.us1.dbt.com`) allows one active project. A second project named NFL was rejected with "You can only have 1 active project on this plan." The existing Partner Connect project was renamed to **NFL**.

| | |
|---|---|
| Project id | `70506183172586` |
| Connection | Databricks, host `dbc-89a97ed5-5f7d.cloud.databricks.com`, HTTP path `/sql/1.0/warehouses/abae422499df211c`, catalog `nfl` |
| Development | environment `70506183161912`, dbt version `fusion-stable` |
| Deployment | environment `70506183161913`, dbt version `fusion-stable` |
| Job | `NFL` (`70506183141641`), commands `dbt build`, generate docs on, schedule off |
| Git | `WyattCurtis327/nfl_dbt_databricks`, branch `main` |

Do not create another project on this plan. A managed Partner Connect repository still exists on the account and is not the project's active repository. `dbt_project.yml` already has `dbt-cloud.project-id` set to this project.

Development credentials, for the Studio IDE, can be your own Databricks user. OAuth is preferred. A personal access token also works. Do not paste that token into this repo.

### 7.3 Deployment environment

The deployment environment already exists (`70506183161913`, `fusion-stable`). Do not create a second one. These are the settings if you ever have to recreate it.

1. **Orchestration → Environments → Create new environment**.
2. Type: **Deployment**.
3. dbt version: **1.12 or newer**, or **v2** (`fusion-stable` is v2). The semantic YAML in this repo is the latest spec. It does not parse on dbt 1.11 or older. The deployment environment here is already `fusion-stable`. On v2, the job must also generate docs (next step). `dbt docs generate` is a job setting on the existing NFL job, not a separate command in the command list.
4. Catalog: `nfl`.
5. Schema: `default`. Custom schemas still land in `bronze`, `silver`, and `gold` because of `generate_schema_name`.
6. Deployment credentials: a Databricks identity that can write those three schemas and read `nfl.landing`. Your user works for a personal project. A service principal is the right production identity. Create one in the Databricks account admin, add it to this workspace, grant it Databricks SQL, and use its token here. Do not commit the token.
7. Save.

### 7.4 Deploy job

The job **NFL** already exists and is not scheduled. Do not create a second job. These are the settings if you ever have to recreate it.

1. **Orchestration → Jobs → Create job → Deploy job**.
2. Environment: the deployment environment from 7.3.
3. Command:

```text
dbt build
```

Turn **Generate docs** on. On the job that exists, that is a setting, not a second command. `dbt build` parses the project as part of the run, which writes `semantic_manifest.json` for that run. `dbt docs generate` is what v2 needs before the Semantic Layer will serve the metrics, and the generate-docs setting is how this job does that.

When this job was updated, `dbt deps`, `dbt parse`, and `dbt docs generate` were rejected as command steps. `dbt build` was accepted. Do not add the rejected commands back unless the job editor accepts them.

4. Turn on a schedule only if you want platform to refresh the tables. The Databricks job in section 8 can do that instead. Do not schedule both, or they will rebuild the same tables.
5. **Run now**. Wait until the run is successful. The run log should show the bronze, silver, and gold models and no failing tests.

### 7.5 Turn on the Semantic Layer

You need to be an Owner on a Starter plan, or have the admin permissions listed in dbt's Semantic Layer setup docs, on Enterprise.

1. **Account settings → Projects → NFL**.
2. **Semantic Layer → Configure Semantic Layer**.
3. Select the deployment environment from 7.3. Save.
4. **Add Semantic Layer credential**. Use a Databricks credential that can **read** `nfl.gold` (and `nfl.silver` / `nfl.bronze` if a metric ever points there). Read-only is enough. Queries run as this credential.
   - Host: `dbc-89a97ed5-5f7d.cloud.databricks.com`
   - HTTP path: `/sql/1.0/warehouses/abae422499df211c`
   - Catalog: `nfl`
5. **Map new service token**. Permissions: **Semantic Layer Only** and **Metadata Only**. Copy the token once. It is not shown again.
6. On the project page, copy the environment id, host, and token for whatever tool will query the metrics.

Personal access tokens also work. **Account settings → Credentials → NFL → Edit**, set your user credentials, then create a personal token under API tokens. Queries then run as you.

### 7.6 Query a metric

After the deploy job is green and the Semantic Layer credential is saved, a tool connected with that token can ask for:

| Metric | Group by |
|---|---|
| `games`, `played_games`, `upset_rate`, `home_cover_rate`, `avg_total_score` | `game__season` or `game__game_week` |
| `team_wins`, `win_percentage`, `points_per_game`, `team_point_differential` | `team_season__team`, `team_season__season` |

Metrics are defined on the models in `models/gold/schema.yml`. Saved queries in `models/gold/semantic_models.yml`: `games_by_season`, `games_by_week`, `team_seasons`.

`metric_time` on games is the calendar date, not the NFL season. A January playoff game counts in the next calendar year. Team-season `metric_time` is `season_start`, January 1 of that season. Group by `game__season` or `team_season__season` when you want the NFL season rather than the calendar year.

## 8. Deploy the Databricks job

This path refreshes tables in Unity Catalog. It does **not** publish the Semantic Layer API. Use it when you want Databricks, not dbt platform, to run `dbt build`.

The bundle is `databricks.yml`. The job is `resources/nfl.job.yml`. It has one task:

```text
dbt deps
dbt build
```

The task uses `dbt_profiles/profiles.yml`. That file reads `DBT_HOST` and `DBT_ACCESS_TOKEN`, which the Databricks dbt task injects. It is not your laptop profile.

The job has **no schedule**. `c:\Users\wyatt\grok\dbt_demo` already has a daily job that builds these same `nfl` tables. A second schedule would rebuild them twice. Add a trigger on this job only after you pause or delete that one.

Commands, from this folder:

```powershell
$env:DATABRICKS_CONFIG_PROFILE = "wyatts_databricks"
databricks bundle validate --target dev --profile wyatts_databricks
databricks bundle deploy --target dev --profile wyatts_databricks
databricks bundle run nfl_job --target dev --profile wyatts_databricks
```

A dev deploy is named `[dev wyatt_curtis] nfl_dbt` (the exact prefix uses your workspace user) and is not production.

Production, still with no schedule until you add one:

```powershell
databricks bundle deploy --target prod --profile wyatts_databricks
databricks bundle run nfl_job --target prod --profile wyatts_databricks
```

To schedule it later, add this under `resources.jobs.nfl_job` in `resources/nfl.job.yml`, then deploy prod again:

```yaml
trigger:
  periodic:
    interval: 1
    unit: DAYS
```

Dev deploys pause that trigger. Prod leaves it on.

## 9. What was already done on this machine

- Profile `nfl` added to `~/.dbt/profiles.yml` (OAuth, no token).
- Project files created in this folder.
- `.venv` installed with dbt Core 1.12.5 and `dbt-databricks` 1.12.6.
- `dbt debug` passed against the Serverless Starter Warehouse and catalog `nfl`.
- `dbt build` completed before the semantic YAML move: 13 tables, 45 tests. `PASS=58`, `ERROR=0`. The SQL models did not change in that move.
- The semantic YAML is the latest spec. A later `dbt parse` on dbt 1.12.5 rewrote `target/semantic_manifest.json` with 2 semantic models (`game_summaries`, `team_performance`), 21 metrics, and 3 saved queries.
- `databricks bundle validate --target dev` succeeded. The job was not deployed and has no schedule.
- The dbt platform account `wyatts_dbt` allows one active project. The Partner Connect project was renamed to **NFL** rather than creating a second one. Project id `70506183172586`. Open it at `https://ib010.us1.dbt.com`.
- That project already uses this workspace, the Serverless Starter Warehouse, and catalog `nfl`. Its development and deployment environments are on `fusion-stable`. The job named `NFL` runs `dbt build` and generates docs. The schedule is off.
- This folder is a git repo on branch `main` with origin `https://github.com/WyattCurtis327/nfl_dbt_databricks.git`. The dbt platform project NFL is linked to that repo.
- `C:\Users\wyatt\.dbt\dbt_cloud.yml` is installed from the credentials file already in Downloads, with the project name set to NFL.

## 10. If something fails

| What you see | What to do |
|---|---|
| `dbt` is not recognized | Activate `.venv`, or call `.\.venv\Scripts\dbt.exe`. |
| `dbt login` is not a command | The active `dbt` is dbt Core. Sign in from the VS Code extension instead. |
| `cannot configure default credentials` or OAuth errors | Re-run the `databricks auth login` command in section 1, then set `DATABRICKS_CONFIG_PROFILE` and the `https://` host fix from section 3. |
| Warehouse timeout on the first command | The Serverless Starter Warehouse was stopped. Run the command again. |
| Extension or `dbt parse` rejects `semantic_models`, `measures`, or `type_params` | This repo uses the latest spec. Metrics are on the model in `models/gold/schema.yml`. Do not put the model in that file and again in `semantic_models.yml`. |
| Semantic Layer returns no metrics | The deploy job in section 7.4 has not succeeded in the environment selected in section 7.5. `dbt build` on the laptop is not enough. On v2, the job also needs `dbt docs generate`. |
| Two jobs writing the same tables | Pause the `dbt_demo` job or this one. Keep a single scheduler. |
