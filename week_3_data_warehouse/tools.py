import os
import pandas as pd
from sqlalchemy import create_engine
import requests
from google.cloud import bigquery, storage

# Get PostgreSQL connection parameters from environment variables
CONN_STR = os.environ.get('DB_URL')
print("Connection string:", CONN_STR)
PARQUET_DIR = 'parquet_data/'

# Google Cloud Platform parameters
GCP_BQ_ID = os.environ.get('GCP_BQ_ID')
GCP_BQ_DATASET_ID = os.environ.get('GCP_BQ_DATASET_ID')
GCP_BQ_TABLE_ID = os.environ.get('GCP_BQ_TABLE_ID')
GCP_GCS_BUCKET_NAME = os.environ.get('GCP_GCS_BUCKET_NAME')


# Function to download Parquet files
def download_parquet():
    os.makedirs(PARQUET_DIR, exist_ok=True)

    # Download Parquet files for each month in 2022
    for month in range(1, 13):
        month = str(month).zfill(2)
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-{month}.parquet"
        file_path = os.path.join(PARQUET_DIR, f"green_tripdata_2022-{month}.parquet")
        response = requests.get(url)
        with open(file_path, 'wb') as f:
            f.write(response.content)

def upload_postgres():
    engine = create_engine(CONN_STR, pool_size=10,
                                max_overflow=2,
                                pool_recycle=300,
                                pool_pre_ping=True,
                                pool_use_lifo=True)
    return engine

def upload_to_gcs(file_dir, file_name):
    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    # Create a bucket object
    bucket = storage_client.bucket(GCP_GCS_BUCKET_NAME)

    # Define the destination blob
    blob = bucket.blob(file_name)

    #write to blob
    blob.upload_from_filename(file_dir)
    print(f'File {file_name} uploaded to GCS bucket {GCP_GCS_BUCKET_NAME}.')

def upload_to_bigquery(df):
    # Initialize BigQuery client
    client = bigquery.Client(project=GCP_BQ_ID)

    # Define BigQuery table reference
    table_ref = f"{GCP_BQ_ID}.{GCP_BQ_DATASET_ID}.{GCP_BQ_TABLE_ID}"

    # Write DataFrame to BigQuery table
    job_config = bigquery.LoadJobConfig(schema=df.dtypes.apply(lambda x: bigquery.SchemaField(x.name, 'STRING')).tolist(), 
                                         write_disposition='WRITE_APPEND')
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Wait for job to complete

    print(f"Data loaded to BigQuery table {table_ref} successfully.")

def gcs_to_bigquery(sql_query):
    # Create a BigQuery client
    client = bigquery.Client(project=GCP_BQ_ID)

    # Execute the SQL query
    for sql in sql_query:    
        query_job = client.query(sql)

def execute_task(Engine=None, GCS=None, BQ=None, query=None):
    try:
        # Get the engine of database
        if Engine:
            engine = upload_postgres()
        
        # Iterate through each Parquet file in the directory
        for file_name in os.listdir(PARQUET_DIR):
            if file_name.endswith('.parquet'):
                file_dir = os.path.join(PARQUET_DIR, file_name)
                
                # Read Parquet file into a pandas DataFrame
                df = pd.read_parquet(file_dir)

                # Insert DataFrame into PostgreSQL table
                if Engine:
                    try:
                        df.to_sql(GCP_BQ_TABLE_ID, engine, if_exists='append', index=False)
                        print('Successfully inserted to PostgreSQL database!')
                    except Exception as e:
                        engine.dispose()
                        print("Failed to connect to PostgreSQL database:", e)

                # Load DataFrame into Storage
                if GCS:
                    try:
                        upload_to_gcs(file_dir, file_name)
                    except Exception as e:
                        print("Failed to upload to Google Cloud Storage:", e)
                
                # Load DataFrame into BigQuery
                if BQ:
                    try:
                        upload_to_bigquery(df)
                    except Exception as e:
                        print("Failed to upload to BigQuery:", e)
    finally:        
        if Engine:
            engine.dispose()
        

if __name__ == '__main__':
    download_parquet()
    execute_task(Engine=True, GCS=True)
    sql_query = [
    f"""
    CREATE OR REPLACE EXTERNAL TABLE `{GCP_BQ_ID}.{GCP_BQ_DATASET_ID}.{GCP_BQ_TABLE_ID}`
    OPTIONS (
    format = 'parquet',
    uris = ['gs://{GCP_GCS_BUCKET_NAME}/*.parquet']
    );
    """, 
    f"""
    CREATE OR REPLACE TABLE `{GCP_BQ_ID}.{GCP_BQ_DATASET_ID}.{GCP_BQ_TABLE_ID}_non_partitoned` AS
    SELECT * FROM `{GCP_BQ_ID}.{GCP_BQ_DATASET_ID}.{GCP_BQ_TABLE_ID}`;
    """, 
    f"""
    CREATE OR REPLACE TABLE `{GCP_BQ_ID}.{GCP_BQ_DATASET_ID}.{GCP_BQ_TABLE_ID}_partitoned`
    PARTITION BY
      DATE(lpep_pickup_datetime) AS
    SELECT * FROM `{GCP_BQ_ID}.{GCP_BQ_DATASET_ID}.{GCP_BQ_TABLE_ID}`;
    """
    ]
    gcs_to_bigquery(sql_query)