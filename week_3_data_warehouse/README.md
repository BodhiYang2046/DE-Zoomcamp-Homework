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
CREATE OR REPLACE EXTERNAL TABLE `crested-axe-412222.homework3.green_taxi`
OPTIONS (
  format = 'parquet',
  uris = ['gs://homework3_bodhi_yang/green_tripdata_2022-*.parquet']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE crested-axe-412222.homework3.green_taxi_non_partitoned AS
SELECT * FROM crested-axe-412222.homework3.green_taxi;


CREATE OR REPLACE TABLE `crested-axe-412222.homework3.green_taxi_partitoned`
PARTITION BY
  DATE(lpep_pickup_datetime) AS
SELECT * FROM `crested-axe-412222.homework3.green_taxi`;

```
