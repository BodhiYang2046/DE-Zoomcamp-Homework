FROM python:3.9

# Install necessary packages
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --no-cache-dir pandas psycopg2 sqlalchemy requests pyarrow google-cloud-storage google-cloud-bigquery

# Copy the Python script into the image
WORKDIR /app
COPY main.py main.py
COPY keys/my-creds.json keys/my-creds.json

# Run the Python script when the container starts
ENTRYPOINT ["python", "main.py"]