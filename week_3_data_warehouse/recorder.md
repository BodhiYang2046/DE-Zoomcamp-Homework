# Loop through each month from January to December
```bash
for month in {01..12}; do
    curl -O "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-${month}.parquet"
done
```

```bash
docker build -t homework3 .  
```

```bash
docker run -d --name database -p 5432:5432 -e POSTGRES_PASSWORD=bodhi postgres:latest
docker run -d --name database homework3

# docker run --name database -d homework3   
```

```bash
docker exec -it database psql -U postgres
```

```sql
CREATE DATABASE green_taxi;
CREATE USER my_user WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE my_database TO my_user;
```

CREATE TABLE green_taxi_2022 (
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
COPY green_taxi_2022 FROM '/parquet_data/green_tripdata_2022-01.parquet' (FORMAT 'parquet');


