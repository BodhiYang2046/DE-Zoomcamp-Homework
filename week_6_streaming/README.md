## Start Red Panda

``` bash
docker-compose up -d
```

进入docker
``` bash
docker-compose exec redpanda-1 bash
```

### Question 1: Redpanda version
``` bash
rpk version
```

### Question 2. Creating a topic
```bash
rpk topic create test-topic
```

## Reading data with rpk

```bash
rpk topic consume test-topic
```
## Sending the taxi data

### Question 5: Sending the Trip Data
```bash
rpk topic create green-trips
```

## Creating the PySpark consumer

```bash
docker network  create kafka-spark-network
docker-compose up -d
```

### Question 6. Parsing the data
