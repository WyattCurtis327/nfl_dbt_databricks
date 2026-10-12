-- One player, team, week, and game type.
select
    season,
    week,
    team,
    gsis_id,
    game_type,
    count(*) as roster_rows
from {{ ref('silver_roster_weeks') }}
group by season, week, team, gsis_id, game_type
having count(*) > 1
