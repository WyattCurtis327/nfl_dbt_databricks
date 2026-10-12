-- Every roster team must exist for that season.
select
    rosters.season,
    rosters.team
from {{ ref('silver_roster_weeks') }} as rosters
left join {{ ref('silver_teams') }} as teams
    on rosters.season = teams.season
    and rosters.team = teams.team
where teams.team is null
