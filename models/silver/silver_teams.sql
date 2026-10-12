{{ config(alias='teams') }}

select
    *,
    lower(trim(full)) as team_name_normalized
from {{ ref('bronze_teams') }}
