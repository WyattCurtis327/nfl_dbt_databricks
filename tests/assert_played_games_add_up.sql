-- Played games must carry a total that matches the two scores.
select
    game_id,
    home_score,
    away_score,
    total_score
from {{ ref('silver_games') }}
where home_score is not null
  and away_score is not null
  and total_score != home_score + away_score
