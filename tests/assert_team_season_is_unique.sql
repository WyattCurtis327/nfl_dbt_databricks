select
    season,
    team,
    count(*) as row_count
from {{ ref('team_performance_by_season') }}
group by season, team
having count(*) > 1
