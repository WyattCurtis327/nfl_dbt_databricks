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
| `dbt-databricks` in `.venv` | dbt Core 1.x plus the Databricks adapter | `dbt build` on your laptop and the Databricks job |
| dbt v2, installed by the VS Code extension | The current dbt engine from dbt Labs | Editor features, and the dbt platform account after you sign in |

`pip install dbt` now installs dbt v2, not dbt Core. This repo pins `dbt-databricks` so the laptop and the Databricks job run the same adapter.

There is no saved dbt platform session on this machine. The Databricks connection is already logged in. The dbt account sign-in is a browser step in [section 4](#4-sign-in-to-your-dbt-account) and again when you create the platform project in [section 7](#7-deploy-the-semantic-layer-on-your-dbt-account).

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

From this folder (`c:\Users\wyatt\grok\dbt_demo2`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
dbt --version
```

`dbt --version` should report dbt Core 1.x and `databricks` under plugins. If PowerShell blocks the activate script:

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

The dbt platform (formerly dbt Cloud) is a separate login from Databricks. Nothing under `~/.dbt` currently holds a platform token. The Cloud CLI zip in `Downloads\dbt_0.40.24_windows_amd64` is also not logged in.

1. Install Visual Studio Code if it is not installed: [https://code.visualstudio.com](https://code.visualstudio.com).
2. Open this folder: **File → Open Folder** → `c:\Users\wyatt\grok\dbt_demo2`.
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
dbt_project.yml          project name nfl, profile nfl
packages.yml             no packages
models/sources.yml       nfl.landing
models/bronze/           landing copy plus audit columns
models/silver/           types, filters, scores
models/gold/             marts, time spine, semantic layer
macros/generate_schema_name.sql
tests/                   singular tests
dbt_profiles/profiles.yml    Databricks job only
databricks.yml           bundle
resources/nfl.job.yml    one dbt task, no schedule
```

A positive `spread_line` means the home team was favored by that many points.

`nfl.bronze.rosters` is a materialized view from another pipeline. This project writes `nfl.bronze.roster_weeks` and does not replace `rosters`.

`nfl.gold.game_pick_metrics` is a Unity Catalog metric view. It is not the dbt Semantic Layer. Leave it alone.

## 6. Build on Databricks from VS Code or the terminal

From an activated `.venv`, with the profile env vars from section 3:

```powershell
dbt deps
dbt build
```

`dbt deps` does nothing useful today (`packages.yml` is empty) and is here so the command matches the job.

`dbt build` runs models and tests. It replaces:

- `nfl.bronze.games`, `teams`, `players`, `game_odds`, `roster_weeks`
- `nfl.silver.games`, `teams`, `players`, `game_odds`, `roster_weeks`
- `nfl.gold.game_summaries`, `team_performance_by_season`, `metricflow_time_spine`

In VS Code, with the dbt extension signed in, you can also right-click a model and run **Build** or **Preview**. Preview uses the extension's dbt v2 engine and the same `nfl` profile.

Check the semantic layer parses:

```powershell
dbt parse
```

After a successful parse, `target/semantic_manifest.json` exists. That file is local. Downstream tools cannot query it until a dbt platform deploy job publishes it (section 7).

Useful narrower commands:

```powershell
dbt build --select gold
dbt test --select team_performance_by_season
dbt show --select game_summaries --limit 20
```

## 7. Deploy the semantic layer on your dbt account

The Semantic Layer API runs only in a dbt platform **deployment** environment. A laptop `dbt build` and a Databricks job do not publish it.

You need a dbt platform plan that includes the Semantic Layer (Starter, Enterprise, or Enterprise+, including a Starter trial). Developer querying against the Semantic Layer is not available yet. Queries hit the deployment environment.

### 7.1 Put the project in Git

dbt platform deploys from a Git repo. This folder is not a Git repo yet.

```powershell
git init
git add .
git commit -m "Add the NFL dbt project"
```

Create an empty GitHub repo (or use the Git host already connected to your dbt account) and push this folder. In dbt platform the Git connection has to be able to read that repo.

### 7.2 Create the dbt platform project

1. Open your dbt account in the browser.
2. **Account settings → Projects → New project**.
3. Name it `NFL`.
4. Connection type: **Databricks**.
5. Server hostname: `dbc-89a97ed5-5f7d.cloud.databricks.com`
6. HTTP path: `/sql/1.0/warehouses/abae422499df211c`
7. Catalog: `nfl` (optional on the connection form; this project also sets `+catalog: nfl` in `dbt_project.yml`).
8. Save, then connect the Git repo from step 7.1. Use the subdirectory only if you did not put `dbt_project.yml` at the repo root. In this folder it is at the root.

Development credentials, for the Studio IDE, can be your own Databricks user. OAuth is preferred. A personal access token also works. Do not paste that token into this repo.

### 7.3 Deployment environment

1. **Orchestration → Environments → Create new environment**.
2. Type: **Deployment**.
3. dbt version: **1.6 or newer**. Use the latest 1.x release track, or **v2** if that is what the account offers. The semantic YAML in this repo is the MetricFlow spec that dbt 1.10+ parses. If the environment is on dbt v2, the job must also run `dbt docs generate` (next step).
4. Catalog: `nfl`.
5. Schema: `default`. Custom schemas still land in `bronze`, `silver`, and `gold` because of `generate_schema_name`.
6. Deployment credentials: a Databricks identity that can write those three schemas and read `nfl.landing`. Your user works for a personal project. A service principal is the right production identity. Create one in the Databricks account admin, add it to this workspace, grant it Databricks SQL, and use its token here. Do not commit the token.
7. Save.

### 7.4 Deploy job

1. **Orchestration → Jobs → Create job → Deploy job**.
2. Environment: the deployment environment from 7.3.
3. Commands, in order:

```text
dbt deps
dbt build
dbt parse
```

If the environment is dbt v2, add this as well:

```text
dbt docs generate
```

`dbt build` materializes the medallion and runs tests. `dbt parse` writes `semantic_manifest.json` (and `osi_document.json` on current versions). `dbt docs generate` is what v2 needs before the Semantic Layer will serve the metrics.

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

Saved queries in `models/gold/semantic_models.yml`: `games_by_season`, `games_by_week`, `team_seasons`.

`metric_time` on games is the calendar date, not the NFL season. A January playoff game counts in the next calendar year. Team-season `metric_time` is January 1 of that season.

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
- `dbt build` completed: 13 tables, 45 tests, 21 metrics, 2 semantic models, 3 saved queries. `PASS=58`, `ERROR=0`.
- `dbt parse` wrote `target/semantic_manifest.json`.
- `databricks bundle validate --target dev` succeeded. The job was not deployed and has no schedule.
- The dbt platform project `NFL` was **not** created. There is no saved dbt platform login on this machine. That needs the browser sign-in in section 4 and the clicks in section 7.

## 10. If something fails

| What you see | What to do |
|---|---|
| `dbt` is not recognized | Activate `.venv`, or call `.\.venv\Scripts\dbt.exe`. |
| `dbt login` is not a command | The active `dbt` is dbt Core. Sign in from the VS Code extension instead. |
| `cannot configure default credentials` or OAuth errors | Re-run the `databricks auth login` command in section 1, then set `DATABRICKS_CONFIG_PROFILE` and the `https://` host fix from section 3. |
| Warehouse timeout on the first command | The Serverless Starter Warehouse was stopped. Run the command again. |
| Extension says the project is not v2 compliant | Use the extension's autofix, or keep building with the venv `dbt`. The YAML in this repo targets dbt 1.10+. |
| Semantic Layer returns no metrics | The deploy job in section 7.4 has not succeeded in the environment selected in section 7.5. `dbt build` on the laptop is not enough. On v2, the job also needs `dbt docs generate`. |
| Two jobs writing the same tables | Pause the `dbt_demo` job or this one. Keep a single scheduler. |
