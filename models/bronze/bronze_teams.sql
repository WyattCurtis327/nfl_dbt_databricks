{{ config(alias='teams') }}

select
    *,
    current_timestamp() as _ingest_timestamp,
    'landing' as _source_schema,
    'teams' as _source_table
from {{ source('landing', 'teams') }}
