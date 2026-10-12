{{ config(alias='roster_weeks') }}

select
    *,
    current_timestamp() as _ingest_timestamp,
    'landing' as _source_schema,
    'rosters' as _source_table
from {{ source('landing', 'rosters') }}
