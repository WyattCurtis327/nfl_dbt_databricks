"""One-shot writer for schema column descriptions. Not part of the dbt project."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def col(name, doc):
    return f"      - name: {name}\n        description: \"{{{{ doc('{doc}') }}}}\""

def block(name, doc, extra=""):
    text = col(name, doc)
    if extra:
        text += "\n" + extra.rstrip("\n")
    return text

TESTS = {
    "bronze_games": {
        "game_id": "        data_tests:\n          - unique\n          - not_null",
    },
    "bronze_teams": {
        "team": "        data_tests:\n          - not_null",
        "season": "        data_tests:\n          - not_null",
    },
    "bronze_players": {
        "player_id": "        data_tests:\n          - unique\n          - not_null",
    },
    "bronze_game_odds": {
        "game_id": "        data_tests:\n          - unique\n          - not_null",
    },
    "bronze_roster_weeks": {
        "season": "        data_tests:\n          - not_null",
        "week": "        data_tests:\n          - not_null",
        "team": "        data_tests:\n          - not_null",
    },
    "silver_games": {
        "game_id": "        data_tests:\n          - unique\n          - not_null",
        "gameday": "        data_tests:\n          - not_null",
        "game_type": "        data_tests:\n          - accepted_values:\n              arguments:\n                values: [\"REG\", \"WC\", \"DIV\", \"CON\", \"SB\"]",
        "home_team": "        data_tests:\n          - not_null\n          - relationships:\n              arguments:\n                to: ref('silver_teams')\n                field: team",
        "away_team": "        data_tests:\n          - not_null\n          - relationships:\n              arguments:\n                to: ref('silver_teams')\n                field: team",
    },
    "silver_teams": {
        "team": "        data_tests:\n          - not_null",
        "season": "        data_tests:\n          - not_null",
    },
    "silver_players": {
        "player_id": "        data_tests:\n          - unique\n          - not_null",
    },
    "silver_roster_weeks": {
        "gsis_id": "        data_tests:\n          - not_null",
        "season": "        data_tests:\n          - not_null",
        "week": "        data_tests:\n          - not_null",
        "team": "        data_tests:\n          - not_null",
        "game_type": "        data_tests:\n          - not_null\n          - accepted_values:\n              arguments:\n                values: [\"REG\", \"WC\", \"DIV\", \"CON\", \"SB\"]",
    },
    "silver_game_odds": {
        "game_id": "        data_tests:\n          - unique\n          - not_null\n          - relationships:\n              arguments:\n                to: ref('silver_games')\n                field: game_id",
    },
}

GAMES = [
    ("game_id", "col_game_id"),
    ("season", "col_season"),
    ("game_type", "col_game_type"),
    ("week", "col_week"),
    ("gameday", "col_gameday_text"),
    ("weekday", "col_weekday"),
    ("gametime", "col_gametime"),
    ("away_team", "col_away_team"),
    ("away_score", "col_away_score"),
    ("home_team", "col_home_team"),
    ("home_score", "col_home_score"),
    ("location", "col_location"),
    ("result", "col_result"),
    ("total", "col_total_points"),
    ("overtime", "col_overtime"),
    ("old_game_id", "col_old_game_id"),
    ("gsis", "col_gsis_game_id"),
    ("nfl_detail_id", "col_nfl_detail_id"),
    ("pfr", "col_pfr_game_id"),
    ("pff", "col_pff_game_id"),
    ("espn", "col_espn_game_id"),
    ("ftn", "col_ftn_game_id"),
    ("away_rest", "col_away_rest"),
    ("home_rest", "col_home_rest"),
    ("away_moneyline", "col_away_moneyline"),
    ("home_moneyline", "col_home_moneyline"),
    ("spread_line", "col_spread_line"),
    ("away_spread_odds", "col_away_spread_odds"),
    ("home_spread_odds", "col_home_spread_odds"),
    ("total_line", "col_total_line"),
    ("under_odds", "col_under_odds"),
    ("over_odds", "col_over_odds"),
    ("div_game", "col_div_game"),
    ("roof", "col_roof"),
    ("surface", "col_surface"),
    ("temp", "col_temp"),
    ("wind", "col_wind"),
    ("away_qb_id", "col_away_qb_id"),
    ("home_qb_id", "col_home_qb_id"),
    ("away_qb_name", "col_away_qb_name"),
    ("home_qb_name", "col_home_qb_name"),
    ("away_coach", "col_away_coach"),
    ("home_coach", "col_home_coach"),
    ("referee", "col_referee"),
    ("stadium_id", "col_stadium_id"),
    ("stadium", "col_stadium"),
    ("ingested_at", "col_ingested_at"),
    ("_source_file", "col_source_file"),
]
AUDIT = [
    ("_ingest_timestamp", "col_ingest_timestamp"),
    ("_source_schema", "col_source_schema"),
    ("_source_table", "col_source_table"),
]
SILVER_GAMES = [c for c in GAMES if c[0] != "gameday"] + [
    ("_ingest_timestamp", "col_ingest_timestamp"),
    ("_source_schema", "col_source_schema"),
    ("_source_table", "col_source_table"),
    ("gameday", "col_gameday_date"),
    ("total_score", "col_total_score"),
    ("point_differential", "col_point_differential"),
]

TEAMS = [
    ("season", "col_season"),
    ("team", "col_team"),
    ("nfl", "col_team_nfl"),
    ("nfl_team_id", "col_nfl_team_id"),
    ("espn", "col_team_espn"),
    ("pfr", "col_team_pfr"),
    ("pff", "col_team_pff"),
    ("pfflabel", "col_pfflabel"),
    ("fo", "col_fo"),
    ("full", "col_full"),
    ("location", "col_team_location"),
    ("short_location", "col_short_location"),
    ("nickname", "col_nickname"),
    ("hyphenated", "col_hyphenated"),
    ("sbr", "col_sbr"),
    ("sbr_wins", "col_sbr_wins"),
    ("sbr_name", "col_sbr_name"),
    ("draft_kings", "col_draft_kings"),
    ("ingested_at", "col_ingested_at"),
    ("_source_file", "col_source_file"),
]
SILVER_TEAMS = TEAMS + AUDIT + [("team_name_normalized", "col_team_name_normalized")]

PLAYERS = [
    ("player_id", "col_player_id"),
    ("gsis_id", "col_gsis_id"),
    ("full_name", "col_full_name"),
    ("player_label", "col_player_label"),
    ("name_collision", "col_name_collision"),
    ("team", "col_team"),
    ("position", "col_player_position"),
    ("jersey_number", "col_jersey_number"),
    ("status", "col_player_status"),
    ("espn_id", "col_espn_id"),
    ("season", "col_season"),
    ("week", "col_player_week"),
    ("ingested_at", "col_ingested_at"),
    ("_source_file", "col_source_file"),
]

ODDS = [
    ("game_id", "col_game_id"),
    ("season", "col_season"),
    ("week", "col_week"),
    ("game_type", "col_game_type"),
    ("gameday", "col_gameday_text"),
    ("home_team", "col_home_team"),
    ("away_team", "col_away_team"),
    ("spread_line", "col_spread_line"),
    ("total_line", "col_total_line"),
    ("away_moneyline", "col_away_moneyline"),
    ("home_moneyline", "col_home_moneyline"),
    ("away_spread_odds", "col_away_spread_odds"),
    ("home_spread_odds", "col_home_spread_odds"),
    ("under_odds", "col_under_odds"),
    ("over_odds", "col_over_odds"),
    ("source", "col_odds_source"),
    ("bookmaker", "col_bookmaker"),
    ("ingested_at", "col_ingested_at"),
    ("_source_file", "col_source_file"),
]
SILVER_ODDS = [c for c in ODDS if c[0] != "gameday"] + AUDIT + [("gameday", "col_gameday_date")]

ROSTER = [
    ("season", "col_season"),
    ("team", "col_team"),
    ("position", "col_player_position"),
    ("depth_chart_position", "col_depth_chart_position"),
    ("jersey_number", "col_jersey_number"),
    ("status", "col_roster_status"),
    ("full_name", "col_full_name"),
    ("first_name", "col_first_name"),
    ("last_name", "col_last_name"),
    ("birth_date", "col_birth_date_text"),
    ("height", "col_height"),
    ("weight", "col_weight"),
    ("college", "col_college"),
    ("gsis_id", "col_gsis_id"),
    ("espn_id", "col_espn_id"),
    ("sportradar_id", "col_sportradar_id"),
    ("yahoo_id", "col_yahoo_id"),
    ("rotowire_id", "col_rotowire_id"),
    ("pff_id", "col_pff_player_id"),
    ("pfr_id", "col_pfr_player_id"),
    ("fantasy_data_id", "col_fantasy_data_id"),
    ("sleeper_id", "col_sleeper_id"),
    ("years_exp", "col_years_exp"),
    ("headshot_url", "col_headshot_url"),
    ("ngs_position", "col_ngs_position"),
    ("week", "col_week"),
    ("game_type", "col_game_type"),
    ("status_description_abbr", "col_status_description_abbr"),
    ("football_name", "col_football_name"),
    ("esb_id", "col_esb_id"),
    ("gsis_it_id", "col_gsis_it_id"),
    ("smart_id", "col_smart_id"),
    ("entry_year", "col_entry_year"),
    ("rookie_year", "col_rookie_year"),
    ("draft_club", "col_draft_club"),
    ("draft_number", "col_draft_number"),
    ("ingested_at", "col_ingested_at"),
    ("_source_file", "col_source_file"),
]
SILVER_ROSTER = [c for c in ROSTER if c[0] != "birth_date"] + AUDIT + [("birth_date", "col_birth_date")]

def columns(model, pairs):
    tests = TESTS.get(model, {})
    lines = []
    for name, doc in pairs:
        lines.append(block(name, doc, tests.get(name, "")))
    return "\n".join(lines)

def model(name, description, pairs):
    return (
        f"  - name: {name}\n"
        f"    description: {description}\n"
        f"    columns:\n"
        f"{columns(name, pairs)}"
    )

bronze = """version: 2

models:
""" + "\n".join([
    model("bronze_games", "Landing games, plus ingest audit columns. Stored as nfl.bronze.games.", GAMES + AUDIT),
    model("bronze_teams", "Landing teams, plus ingest audit columns. Stored as nfl.bronze.teams.", TEAMS + AUDIT),
    model("bronze_players", "Landing players, plus ingest audit columns. Stored as nfl.bronze.players.", PLAYERS + AUDIT),
    model("bronze_game_odds", "Landing closing lines, plus ingest audit columns. Stored as nfl.bronze.game_odds.", ODDS + AUDIT),
    model("bronze_roster_weeks", "Landing weekly rosters, plus ingest audit columns. Stored as nfl.bronze.roster_weeks. Does not replace nfl.bronze.rosters.", ROSTER + AUDIT),
]) + "\n"

silver = """version: 2

models:
""" + "\n".join([
    model("silver_games", "Games with a real game date, total score, and home point differential. Stored as nfl.silver.games.", SILVER_GAMES),
    model("silver_teams", "Teams with a normalized full name. One row per season and team abbreviation. Stored as nfl.silver.teams.", SILVER_TEAMS),
    model("silver_players", "Players with a player id. Stored as nfl.silver.players.", PLAYERS + AUDIT),
    model("silver_roster_weeks", "Weekly rosters with a player id and birth date as a date. Stored as nfl.silver.roster_weeks.", SILVER_ROSTER),
    model("silver_game_odds", "One closing line per game, with gameday as a date. Stored as nfl.silver.game_odds.", SILVER_ODDS),
]) + "\n"

def source_table(name, description, pairs):
    body = f"      - name: {name}\n"
    if description:
        body += f"        description: {description}\n"
    body += "        columns:\n"
    body += "\n".join(col(n, d).replace("      -", "          -", 1).replace("        description", "            description") for n, d in pairs)
    return body

# fix indent more carefully
def source_cols(pairs):
    lines = []
    for name, doc in pairs:
        lines.append(f"          - name: {name}\n            description: \"{{{{ doc('{doc}') }}}}\"")
    return "\n".join(lines)

sources = f"""version: 2

sources:
  - name: landing
    description: Raw NFL tables already loaded in Unity Catalog. This project does not ingest them.
    database: nfl
    schema: landing
    tables:
      - name: games
        description: NFL schedule and results from the nflverse schedules release.
        columns:
{source_cols(GAMES)}
      - name: teams
        description: One row per season and team abbreviation from the nflverse teams table.
        columns:
{source_cols(TEAMS)}
      - name: players
        description: Player rows already loaded in landing. One row per player, season, and week.
        columns:
{source_cols(PLAYERS)}
      - name: game_odds
        description: Closing lines. One row per game in the current landing table.
        columns:
{source_cols(ODDS)}
      - name: rosters
        description: Weekly rosters. One row per player, team, week, and game type.
        columns:
{source_cols(ROSTER)}
"""

(ROOT / "models" / "bronze" / "schema.yml").write_text(bronze, encoding="utf-8", newline="\n")
(ROOT / "models" / "silver" / "schema.yml").write_text(silver, encoding="utf-8", newline="\n")
(ROOT / "models" / "sources.yml").write_text(sources, encoding="utf-8", newline="\n")
print("wrote bronze", bronze.count("description:"), "silver", silver.count("description:"), "sources", sources.count("description:"))
