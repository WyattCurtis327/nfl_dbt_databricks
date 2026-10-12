{% docs col_game_id %}
nflverse game id. Usually the season, week, away team, and home team joined with underscores.
{% enddocs %}

{% docs col_season %}
NFL season year.
{% enddocs %}

{% docs col_game_type %}
Schedule type. REG is the regular season, WC wild card, DIV divisional, CON conference championship, and SB the Super Bowl.
{% enddocs %}

{% docs col_week %}
Week number inside the season.
{% enddocs %}

{% docs col_gameday_text %}
Game date, stored as text from landing.
{% enddocs %}

{% docs col_gameday_date %}
Game date.
{% enddocs %}

{% docs col_weekday %}
Day of the week the game is played.
{% enddocs %}

{% docs col_gametime %}
Scheduled kickoff time, stored as text.
{% enddocs %}

{% docs col_away_team %}
Away team abbreviation.
{% enddocs %}

{% docs col_away_score %}
Away team final score. Null when the game has not been played.
{% enddocs %}

{% docs col_home_team %}
Home team abbreviation.
{% enddocs %}

{% docs col_home_score %}
Home team final score. Null when the game has not been played.
{% enddocs %}

{% docs col_location %}
Home or Neutral.
{% enddocs %}

{% docs col_result %}
Home score minus away score. Positive means the home team won by that many points. Null when the game has not been played.
{% enddocs %}

{% docs col_total_points %}
Home score plus away score. This is the combined score, not the betting total.
{% enddocs %}

{% docs col_overtime %}
1 when the game went to overtime, otherwise 0.
{% enddocs %}

{% docs col_old_game_id %}
Older nflverse game id.
{% enddocs %}

{% docs col_gsis_game_id %}
GSIS game id.
{% enddocs %}

{% docs col_nfl_detail_id %}
NFL detail id for the game.
{% enddocs %}

{% docs col_pfr_game_id %}
Pro Football Reference game id.
{% enddocs %}

{% docs col_pff_game_id %}
Pro Football Focus game id. Not a PFF grade.
{% enddocs %}

{% docs col_espn_game_id %}
ESPN game id. Not an ESPN score or metric.
{% enddocs %}

{% docs col_ftn_game_id %}
FTN Data game id. Not a Football Reference id.
{% enddocs %}

{% docs col_away_rest %}
Days since the away team previous game.
{% enddocs %}

{% docs col_home_rest %}
Days since the home team previous game.
{% enddocs %}

{% docs col_away_moneyline %}
American odds for the away team to win outright.
{% enddocs %}

{% docs col_home_moneyline %}
American odds for the home team to win outright.
{% enddocs %}

{% docs col_spread_line %}
Closing spread for the home team. Negative means the home team was favored by that many points.
{% enddocs %}

{% docs col_away_spread_odds %}
American odds for the away team to cover the spread.
{% enddocs %}

{% docs col_home_spread_odds %}
American odds for the home team to cover the spread.
{% enddocs %}

{% docs col_total_line %}
Closing total. The combined score the over and the under are set against.
{% enddocs %}

{% docs col_under_odds %}
American odds for the under.
{% enddocs %}

{% docs col_over_odds %}
American odds for the over.
{% enddocs %}

{% docs col_div_game %}
1 when the two teams share a division, otherwise 0.
{% enddocs %}

{% docs col_roof %}
Stadium roof: dome, outdoors, closed, or open.
{% enddocs %}

{% docs col_surface %}
Playing surface, such as grass or a named turf.
{% enddocs %}

{% docs col_temp %}
Kickoff temperature in Fahrenheit. Often missing for indoor games.
{% enddocs %}

{% docs col_wind %}
Kickoff wind speed in miles per hour. Often missing for indoor games.
{% enddocs %}

{% docs col_away_qb_id %}
GSIS id of the away starting quarterback.
{% enddocs %}

{% docs col_home_qb_id %}
GSIS id of the home starting quarterback.
{% enddocs %}

{% docs col_away_qb_name %}
Name of the away starting quarterback.
{% enddocs %}

{% docs col_home_qb_name %}
Name of the home starting quarterback.
{% enddocs %}

{% docs col_away_coach %}
Away head coach.
{% enddocs %}

{% docs col_home_coach %}
Home head coach.
{% enddocs %}

{% docs col_referee %}
Referee assigned to the game.
{% enddocs %}

{% docs col_stadium_id %}
Stadium id.
{% enddocs %}

{% docs col_stadium %}
Stadium name.
{% enddocs %}

{% docs col_ingested_at %}
When the landing job wrote this row.
{% enddocs %}

{% docs col_source_file %}
File the landing job read for this row.
{% enddocs %}

{% docs col_ingest_timestamp %}
When dbt copied this row from landing.
{% enddocs %}

{% docs col_source_schema %}
Schema this row was copied from. Always landing.
{% enddocs %}

{% docs col_source_table %}
Landing table this row was copied from.
{% enddocs %}

{% docs col_odds_source %}
Where the line came from. nflverse is the closing line carried on the schedule file.
{% enddocs %}

{% docs col_bookmaker %}
Book that priced the line. nflverse when the line is the schedule file closing number.
{% enddocs %}

{% docs col_team %}
Team abbreviation.
{% enddocs %}

{% docs col_team_nfl %}
Team abbreviation used by the NFL. Usually the same as team.
{% enddocs %}

{% docs col_nfl_team_id %}
Numeric NFL team id.
{% enddocs %}

{% docs col_team_espn %}
ESPN team abbreviation.
{% enddocs %}

{% docs col_team_pfr %}
Pro Football Reference team abbreviation.
{% enddocs %}

{% docs col_team_pff %}
Pro Football Focus team id. Not a grade.
{% enddocs %}

{% docs col_pfflabel %}
Short Pro Football Focus label. Usually the team abbreviation.
{% enddocs %}

{% docs col_fo %}
Football Outsiders team abbreviation.
{% enddocs %}

{% docs col_full %}
Team name, city and nickname.
{% enddocs %}

{% docs col_team_location %}
City name.
{% enddocs %}

{% docs col_short_location %}
Short city name.
{% enddocs %}

{% docs col_nickname %}
Nickname only, without the city.
{% enddocs %}

{% docs col_hyphenated %}
Lowercase hyphenated team name.
{% enddocs %}

{% docs col_sbr %}
Sportsbook Review team id.
{% enddocs %}

{% docs col_sbr_wins %}
Sportsbook Review win total. Often blank.
{% enddocs %}

{% docs col_sbr_name %}
Sportsbook Review team name.
{% enddocs %}

{% docs col_draft_kings %}
Name DraftKings uses for the team.
{% enddocs %}

{% docs col_team_name_normalized %}
full, lowercased and trimmed.
{% enddocs %}

{% docs col_player_id %}
GSIS player id. On this table it is the same value as gsis_id.
{% enddocs %}

{% docs col_gsis_id %}
GSIS player id.
{% enddocs %}

{% docs col_full_name %}
Player full name.
{% enddocs %}

{% docs col_player_label %}
Display name. Adds the team abbreviation in parentheses when name_collision is true.
{% enddocs %}

{% docs col_name_collision %}
True when player_label includes the team abbreviation.
{% enddocs %}

{% docs col_player_position %}
Roster position, such as QB, WR, or DL.
{% enddocs %}

{% docs col_jersey_number %}
Jersey number.
{% enddocs %}

{% docs col_player_status %}
Roster status code. ACT is active.
{% enddocs %}

{% docs col_espn_id %}
ESPN player id.
{% enddocs %}

{% docs col_player_week %}
Week this player row belongs to.
{% enddocs %}

{% docs col_depth_chart_position %}
Depth-chart position. It can differ from position.
{% enddocs %}

{% docs col_roster_status %}
Roster status. ACT is active, DEV is a practice-squad or development list, RES is reserve, INA is inactive, CUT is released, and RET is retired.
{% enddocs %}

{% docs col_first_name %}
Player first name.
{% enddocs %}

{% docs col_last_name %}
Player last name.
{% enddocs %}

{% docs col_birth_date_text %}
Birth date, stored as text from landing.
{% enddocs %}

{% docs col_birth_date %}
Birth date.
{% enddocs %}

{% docs col_height %}
Height in inches.
{% enddocs %}

{% docs col_weight %}
Weight in pounds.
{% enddocs %}

{% docs col_college %}
College.
{% enddocs %}

{% docs col_sportradar_id %}
Sportradar player id.
{% enddocs %}

{% docs col_yahoo_id %}
Yahoo player id.
{% enddocs %}

{% docs col_rotowire_id %}
RotoWire player id.
{% enddocs %}

{% docs col_pff_player_id %}
Pro Football Focus player id.
{% enddocs %}

{% docs col_pfr_player_id %}
Pro Football Reference player id.
{% enddocs %}

{% docs col_fantasy_data_id %}
FantasyData player id.
{% enddocs %}

{% docs col_sleeper_id %}
Sleeper player id.
{% enddocs %}

{% docs col_years_exp %}
Seasons of experience. 0 is a rookie.
{% enddocs %}

{% docs col_headshot_url %}
URL of the player headshot.
{% enddocs %}

{% docs col_ngs_position %}
Next Gen Stats position.
{% enddocs %}

{% docs col_status_description_abbr %}
Short NFL status code paired with status.
{% enddocs %}

{% docs col_football_name %}
Name on the jersey.
{% enddocs %}

{% docs col_esb_id %}
NFL electronic registration id.
{% enddocs %}

{% docs col_gsis_it_id %}
GSIS internal player id.
{% enddocs %}

{% docs col_smart_id %}
NFL smart id.
{% enddocs %}

{% docs col_entry_year %}
Year the player entered the league.
{% enddocs %}

{% docs col_rookie_year %}
Rookie season.
{% enddocs %}

{% docs col_draft_club %}
Team that drafted the player. Blank when the player was undrafted.
{% enddocs %}

{% docs col_draft_number %}
Overall draft pick. Blank when the player was undrafted.
{% enddocs %}

{% docs col_total_score %}
Home score plus away score. Null when either score is null.
{% enddocs %}

{% docs col_point_differential %}
Home score minus away score. Positive means the home team won. Null when either score is null.
{% enddocs %}

{% docs col_avg_spread %}
Closing spread for the home team, taken from silver game odds. Negative means the home team was favored. That table has one row per game, so this is that line rather than an average of books.
{% enddocs %}

{% docs col_avg_total %}
Closing total, taken from silver game odds.
{% enddocs %}

{% docs col_num_bookmakers %}
Always 1. Silver game odds keeps one closing line per game.
{% enddocs %}

{% docs col_is_upset %}
True when the away team wins and the spread is positive, or the home team wins and the spread is negative. False for every other scored game with a non-zero spread. Null when the score or the spread is missing, or the spread is zero. The stored spread uses the opposite sign: negative means the home team was favored.
{% enddocs %}

{% docs col_beat_spread %}
True when the home score minus the away score is greater than the closing spread. False when both are present and that test fails, including a push. Null when the score or the spread is missing.
{% enddocs %}

{% docs col_over_under_result %}
over when the combined score is above the closing total, under when it is below, and push when it ties. Null when the score or the total is missing.
{% enddocs %}

{% docs col_home_games %}
Played games as the home team. Zero when the team had no played home games. A game counts only when both scores are present.
{% enddocs %}

{% docs col_home_wins %}
Wins as the home team. A tie is not a win. Zero when the team had no played home games.
{% enddocs %}

{% docs col_avg_home_score %}
Average points scored in played home games. Null when the team had no played home games.
{% enddocs %}

{% docs col_avg_home_opponent_score %}
Average points allowed in played home games. Null when the team had no played home games.
{% enddocs %}

{% docs col_away_games %}
Played games as the away team. Zero when the team had no played away games.
{% enddocs %}

{% docs col_away_wins %}
Wins as the away team. A tie is not a win. Zero when the team had no played away games.
{% enddocs %}

{% docs col_avg_away_score %}
Average points scored in played away games. Null when the team had no played away games.
{% enddocs %}

{% docs col_avg_away_opponent_score %}
Average points allowed in played away games. Null when the team had no played away games.
{% enddocs %}

{% docs col_total_games %}
Played home games plus played away games.
{% enddocs %}

{% docs col_total_wins %}
Home wins plus away wins. A tie is not a win.
{% enddocs %}

{% docs col_win_percentage %}
Total wins divided by played games.
{% enddocs %}

{% docs col_avg_points_scored %}
Points scored divided by played games.
{% enddocs %}

{% docs col_avg_points_allowed %}
Points allowed divided by played games.
{% enddocs %}

{% docs col_season_point_differential %}
Points scored minus points allowed across played games. This is the season total, not a per-game average.
{% enddocs %}

{% docs col_date_day %}
One calendar date. The spine runs from 2024-01-01 through 2028-02-15.
{% enddocs %}
