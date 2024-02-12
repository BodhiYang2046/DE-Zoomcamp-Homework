CREATE TABLE parquet_data (
    vendor_id INTEGER,
    passenger_count INTEGER,
    trip_distance numeric,
    ratecode_id INTEGER,
    store_and_fwd_flag text,
    pulocation_id INTEGER,
    dolocation_id INTEGER,
    payment_type INTEGER,
    fare_amount numeric,
    extra numeric,
    mta_tax numeric,
    tip_amount numeric,
    tolls_amount numeric,
    improvement_surcharge numeric,
    total_amount numeric,
    congestion_surcharge numeric,
    lpep_pickup_datetime TIMESTAMP,
    lpep_dropoff_datetime TIMESTAMP,
    ehail_fee numeric,
    trip_type numeric,
    lpep_pickup_date DATE);

-- Use COPY command to import Parquet data into PostgreSQL
COPY parquet_data FROM '/path/to/parquet/files' DELIMITER ',' CSV HEADER;
