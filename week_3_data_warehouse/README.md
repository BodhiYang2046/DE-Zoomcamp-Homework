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
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=bodhi  --name database homework3


# docker run --name database -d homework3   
```

```bash
docker exec -it database psql -U postgres
```

psql -h db -U bodhi -d green_taxi -p 5432

