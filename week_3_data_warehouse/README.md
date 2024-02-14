<!-- ```bash
for month in {01..12}; do
    curl -O "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-${month}.parquet"
done
``` -->

<!-- ```bash
docker build -t homework3 .  
``` -->

<!-- ```bash
docker run -d --name database homework3
docker run --name database -d homework3
docker exec -it database psql -U postgres
``` -->

```bash
docker-compose build
docker-compose up
```

```bash
docker-compose exec db bash 
```

```bash(in container)
psql -h db -U bodhi -d green_taxi -p 5432
```

```bash
mkdir /db
pg_dump -U bodhi -d green_taxi -h host.docker.internal -p 3212 > /db/table.sql
```


```bash
terraform init
terraform apply
```

```sql
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `crested-axe-412222.green_taxi.green_taxi_2022`
OPTIONS (
  format = 'parquet',
  uris = ['gs://de-zoomcamp-homework3-bodhi-yang/green_tripdata_2022-*.parquet']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE `crested-axe-412222.green_taxi.green_taxi_2022_non_partitoned` AS
SELECT * FROM `crested-axe-412222.green_taxi.green_taxi_2022`;

-- question1
select count(1)
from `crested-axe-412222.green_taxi.green_taxi_2022`;

-- question2
SELECT count(DISTINCT PULocationID)
FROM `crested-axe-412222.green_taxi.green_taxi_2022`;

SELECT count(DISTINCT PULocationID)
FROM `crested-axe-412222.green_taxi.green_taxi_2022_non_partitoned`;

-- question3
SELECT count(1)
FROM `crested-axe-412222.green_taxi.green_taxi_2022`
where fare_amount=0;

-- question4
CREATE OR REPLACE TABLE `crested-axe-412222.green_taxi.green_taxi_2022_new`
PARTITION BY
  DATE(lpep_pickup_datetime) 
CLUSTER BY
  PUlocationID AS
SELECT * FROM `crested-axe-412222.green_taxi.green_taxi_2022`;

select PUlocationID
from  `crested-axe-412222.green_taxi.green_taxi_2022_new`
where DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30'
order by PUlocationID;

-- question4
select PUlocationID
from  `crested-axe-412222.green_taxi.green_taxi_2022_new`
where DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30'
order by PUlocationID;

-- question5
select distinct PULocationID
from  `crested-axe-412222.green_taxi.green_taxi_2022_non_partitoned`
where DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

select distinct PULocationID
from  `crested-axe-412222.green_taxi.green_taxi_2022_new`
where DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

-- question8
SELECT count(*)
from  `crested-axe-412222.green_taxi.green_taxi_2022_non_partitoned`

```
