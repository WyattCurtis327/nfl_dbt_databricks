{{ config(alias='players') }}

select *
from {{ ref('bronze_players') }}
where player_id is not null
