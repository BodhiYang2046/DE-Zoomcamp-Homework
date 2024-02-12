import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import requests

# Get PostgreSQL connection parameters from environment variables
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'green_taxi')
DB_USER = os.environ.get('DB_USER', 'bodhi')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'bodhi')

# Create a PostgreSQL connection
conn_str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(conn_str)

with engine.connect() as connection:
    connection.execute(f"CREATE DATABASE {DB_NAME};")
    connection.execute(f"CREATE USER {DB_USER} WITH ENCRYPTED PASSWORD '{DB_PASSWORD}';")
    connection.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};")

# Directory containing Parquet files
parquet_dir = 'parquet_data/'
if not os.path.exists('parquet_data'):
    os.makedirs('parquet_data')

# Function to download Parquet files
def download_parquet(month):
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-{month}.parquet"
    file_path = os.path.join(parquet_dir, f"green_tripdata_2022-{month}.parquet")
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)

# Download Parquet files for each month in 2022
for month in range(1, 13):
    download_parquet(str(month).zfill(2))

# Iterate through each Parquet file in the directory
for file_name in os.listdir(parquet_dir):
    if file_name.endswith('.parquet'):
        # Read Parquet file into a pandas DataFrame
        df = pd.read_parquet(os.path.join(parquet_dir, file_name))

        # Insert DataFrame into PostgreSQL table
        df.to_sql('green_taxi_2022', engine, if_exists='append', index=False)

# Close the database connection
engine.dispose()
