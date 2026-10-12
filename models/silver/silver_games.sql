{{ config(alias='games') }}

select
    * except (gameday),
    cast(gameday as date) as gameday,
    home_score + away_score as total_score,
    home_score - away_score as point_differential
from {{ ref('bronze_games') }}
