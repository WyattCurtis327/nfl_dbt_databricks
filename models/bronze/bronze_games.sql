{{ config(alias='games') }}

select
    *,
    current_timestamp() as _ingest_timestamp,
    'landing' as _source_schema,
    'games' as _source_table
from {{ source('landing', 'games') }}
