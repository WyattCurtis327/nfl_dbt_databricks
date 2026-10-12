with played as (
    select *
    from {{ ref('silver_games') }}
    where home_score is not null
      and away_score is not null
),

home as (
    select
        season,
        home_team as team,
        count(*) as home_games,
        sum(case when home_score > away_score then 1 else 0 end) as home_wins,
        avg(home_score) as avg_home_score,
        avg(away_score) as avg_home_opponent_score,
        sum(home_score) as home_points,
        sum(away_score) as home_points_allowed
    from played
    group by season, home_team
),

away as (
    select
        season,
        away_team as team,
        count(*) as away_games,
        sum(case when away_score > home_score then 1 else 0 end) as away_wins,
        avg(away_score) as avg_away_score,
        avg(home_score) as avg_away_opponent_score,
        sum(away_score) as away_points,
        sum(home_score) as away_points_allowed
    from played
    group by season, away_team
)

select
    coalesce(home.season, away.season) as season,
    coalesce(home.team, away.team) as team,
    coalesce(home.home_games, 0) as home_games,
    coalesce(home.home_wins, 0) as home_wins,
    home.avg_home_score,
    home.avg_home_opponent_score,
    coalesce(away.away_games, 0) as away_games,
    coalesce(away.away_wins, 0) as away_wins,
    away.avg_away_score,
    away.avg_away_opponent_score,
    coalesce(home.home_games, 0) + coalesce(away.away_games, 0) as total_games,
    coalesce(home.home_wins, 0) + coalesce(away.away_wins, 0) as total_wins,
    (coalesce(home.home_wins, 0) + coalesce(away.away_wins, 0))
        / (coalesce(home.home_games, 0) + coalesce(away.away_games, 0)) as win_percentage,
    (coalesce(home.home_points, 0) + coalesce(away.away_points, 0))
        / (coalesce(home.home_games, 0) + coalesce(away.away_games, 0)) as avg_points_scored,
    (coalesce(home.home_points_allowed, 0) + coalesce(away.away_points_allowed, 0))
        / (coalesce(home.home_games, 0) + coalesce(away.away_games, 0)) as avg_points_allowed,
    (coalesce(home.home_points, 0) + coalesce(away.away_points, 0))
        - (coalesce(home.home_points_allowed, 0) + coalesce(away.away_points_allowed, 0)) as point_differential
from home
full outer join away
    on home.season = away.season
    and home.team = away.team
