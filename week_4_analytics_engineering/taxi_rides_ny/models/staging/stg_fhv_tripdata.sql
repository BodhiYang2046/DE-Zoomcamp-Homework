{{
    config(
        materialized='view'
    )
}}

with fhv_tripdata as 
(
  select *,
  from {{ source('staging','fhv_tripdata') }}
)
select *
from fhv_tripdata
where substring(cast (pickup_datetime as STRING),1,4)='2019'


-- dbt build --select <model.sql> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}