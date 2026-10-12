{{ config(alias='game_odds') }}

select
    *,
    current_timestamp() as _ingest_timestamp,
    'landing' as _source_schema,
    'game_odds' as _source_table
from {{ source('landing', 'game_odds') }}
