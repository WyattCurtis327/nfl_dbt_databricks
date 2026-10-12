{{ config(alias='metricflow_time_spine') }}

select explode(sequence(date '2024-01-01', date '2028-02-15', interval 1 day)) as date_day
