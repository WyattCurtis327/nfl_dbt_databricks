{{ config(alias='game_odds') }}

select
    * except (gameday),
    cast(gameday as date) as gameday
from {{ ref('bronze_game_odds') }}
