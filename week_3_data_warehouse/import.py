import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import requests

# Get PostgreSQL connection parameters from environment variables
P_HOST = os.environ.get('P_HOST')
P_PORT = os.environ.get('P_PORT')
P_NAME = os.environ.get('P_NAME')
P_USER = os.environ.get('P_USER')
P_PASSWORD = os.environ.get('P_PASSWORD')
CONN_STR = f'postgresql://{P_USER}:{P_PASSWORD}@{P_HOST}:{P_PORT}/{P_NAME}'
print("Connection string:", CONN_STR)
PARQUET_DIR = 'parquet_data/'

# Function to download Parquet files
def download_parquet(month):
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-{month}.parquet"
    file_path = os.path.join(PARQUET_DIR, f"green_tripdata_2022-{month}.parquet")
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)

def connection():
    try:
        conn = psycopg2.connect(
            dbname=P_NAME,
            user=P_USER,
            password=P_PASSWORD,
            host=P_HOST,
            port=P_PORT
        )
        print("Successfully connected to PostgreSQL database!")
        conn.close()
        download_insert()
    except Exception as e:
        print("Failed to connect to PostgreSQL database:", e)

def download_insert():
    # Directory containing Parquet files
    os.makedirs(PARQUET_DIR, exist_ok=True)

    # Download Parquet files for each month in 2022
    for month in range(1, 13):
        download_parquet(str(month).zfill(2))

    # Create a PostgreSQL connection
    engine = create_engine(CONN_STR, pool_size=10,
                                      max_overflow=2,
                                      pool_recycle=300,
                                      pool_pre_ping=True,
                                      pool_use_lifo=True)

    # Iterate through each Parquet file in the directory
    for file_name in os.listdir(PARQUET_DIR):
        if file_name.endswith('.parquet'):
            # Read Parquet file into a pandas DataFrame
            df = pd.read_parquet(os.path.join(PARQUET_DIR, file_name))
            # Insert DataFrame into PostgreSQL table
            df.to_sql('green_taxi_2022', engine, if_exists='append', index=False)
            print('Successfully inserted to PostgreSQL database!')

    # Close the database connection
    engine.dispose()

if __name__ == '__main__':
    connection()