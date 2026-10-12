{{ config(alias='roster_weeks') }}

select
    * except (birth_date),
    cast(birth_date as date) as birth_date
from {{ ref('bronze_roster_weeks') }}
where gsis_id is not null
