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
## Tutorial

### Step 1: Configure Terraform for Google Cloud Platform (GCP)
Define variables in `variables.tf` for project ID, region, service account key file path, and other necessary parameters.
Use the google provider in `main.tf` to configure Terraform to work with GCP.
Use Terraform resources to create GCP resources such as a BigQuery dataset, Cloud Storage bucket, and service account
```bash
terraform init
terraform apply
```

### Step 2: Set Up Docker Environment
Create Docker Compose File: Create a `docker-compose.yaml` file in my project directory with configurations for PostgreSQL, pgAdmin, and my application container.

### Step 3: Create Dockerfile for My Application
Create a `Dockerfile` in my project directory to define the environment for my Python application.

### Step 4: Write Python Script for My Application
Write a Python script `tools.py` that downloads data, stores it in the PostgreSQL database, uploads it to Google Cloud Storage, and executes SQL commands in BigQuery.

### Step 5: Build and Run Docker Containers
Build my Docker containers:
```bash
docker-compose up
```
Run my Docker containers:
```bash
docker-compose up
```

### Step 5: Access PostgreSQL Database and pgAdmin
```bash
docker-compose exec db bash 
```

(in container)
```bash
psql -h db -U bodhi -d green_taxi -p 3212
```

```bash
mkdir /db
pg_dump -U bodhi -d green_taxi -h host.docker.internal -p 3212 > /db/table.sql
```

### Step 6: Monitor Data Upload to GCS and BigQuery and Complete homework
Check Google Cloud Storage to verify that my data has been uploaded successfully.
Check BigQuery to ensure that my SQL commands have been executed correctly.
Execute sql in BigQuery.

### BigQuery ML


### BigQuery Deployment

#### 1.This command prompts you to authenticate to Google Cloud Platform (GCP) using your Google account. It sets up authentication credentials that allow you to interact with GCP services using the Google Cloud SDK.

```bash
gcloud auth login
```

#### 2.This command uses the BigQuery CLI (bq) to extract a model named green_taxi.tip_model from a BigQuery project with the ID crested-axe-412222 and saves it to Google Cloud Storage (GCS) bucket gs://de-zoomcamp-homework3-bodhi-yang/tip_model.

```bash
bq --project_id crested-axe-412222 extract -m green_taxi.tip_hyperparam_model gs://de-zoomcamp-homework3-bodhi-yang/tip_model
```

#### 3
```bash
mkdir /tmp/model
```

#### 4.This command copies the contents of the tip_model directory from the specified GCS bucket (gs://de-zoomcamp-homework3-bodhi-yang/tip_model) to the local /tmp/model directory.

```bash
gsutil cp -r gs://de-zoomcamp-homework3-bodhi-yang/tip_model /tmp/model
```

#### 5.This command creates a directory structure for serving the model. It creates a directory tip_model within the serving_dir directory, and within that, it creates a subdirectory 1.

```bash
mkdir -p serving_dir/tip_model/1
```

#### 6.This command copies all the contents of the /tmp/model/tip_model directory to the serving_dir/tip_model/1 directory, which was created in the previous step. It's essentially moving the model files into a directory structure expected by TensorFlow Serving.

```bash
cp -r /tmp/model/tip_model/* serving_dir/tip_model/1
```

#### 7.This command pulls the Docker image for TensorFlow Serving from the Docker Hub repository. Docker images are pre-packaged software bundles that contain everything needed to run a piece of software, including the code, runtime, libraries, and dependencies.

```bash
docker pull bitnami/tensorflow-serving:2
```

#### 8.This command runs a Docker container based on the TensorFlow Serving image previously pulled. It exposes port 8501 on the host system (your computer) and mounts the serving_dir/tip_model directory to /models/tip_model inside the container. It also sets the environment variable MODEL_NAME to tip_model.

```bash
docker run -d -p 8501:8501 -v $(pwd)/serving_dir/tip_model/1:/bitnami/model-data/1 -e MODEL_NAME=tip_model -t bitnami/tensorflow-serving:2 
```

#### 9.This command sends a POST request to the TensorFlow Serving server running locally (http://localhost:8501) with data for prediction. It sends a JSON payload containing input features for prediction.

```bash
curl -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' -X POST http://localhost:8501/v1//model-data/tip_model:predict
```


## Homework3

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
from  `crested-axe-412222.green_taxi.green_taxi_2022_non_partitoned`
where DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30'
order by PUlocationID;

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
from  `crested-axe-412222.green_taxi.green_taxi_2022_non_partitoned`;

```
