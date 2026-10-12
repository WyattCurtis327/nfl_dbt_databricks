with odds as (
    select
        game_id,
        spread_line as avg_spread,
        total_line as avg_total,
        cast(1 as bigint) as num_bookmakers
    from {{ ref('silver_game_odds') }}
)

select
    games.game_id,
    games.season,
    games.week,
    games.game_type,
    games.gameday,
    games.home_team,
    games.away_team,
    games.home_score,
    games.away_score,
    games.total_score,
    games.point_differential,
    odds.avg_spread,
    odds.avg_total,
    odds.num_bookmakers,
    -- spread_line is points the home team is favored by. Positive means home is laying points.
    case
        when games.home_score is null or odds.avg_spread is null or odds.avg_spread = 0 then null
        when odds.avg_spread > 0 and games.away_score > games.home_score then true
        when odds.avg_spread < 0 and games.home_score > games.away_score then true
        else false
    end as is_upset,
    case
        when games.home_score is null or odds.avg_spread is null then null
        when games.point_differential - odds.avg_spread > 0 then true
        else false
    end as beat_spread,
    case
        when games.total_score is null or odds.avg_total is null then null
        when games.total_score > odds.avg_total then 'over'
        when games.total_score < odds.avg_total then 'under'
        else 'push'
    end as over_under_result
from {{ ref('silver_games') }} as games
left join odds
    on games.game_id = odds.game_id
