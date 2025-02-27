import argparse
import requests
import pandas as pd
from google.cloud import bigquery
import pyarrow.parquet as pq
from io import BytesIO
from datetime import datetime  # Cleaner import


def download_parquet(url):
    
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Successfully downloaded data from {url}")
        return BytesIO(response.content)
    else:
        print(f"Failed to download: {url}")
        return None

def transform_data(parquet_file, taxi_type):

    df = pd.read_parquet(parquet_file)

    if taxi_type == "yellow":
        #Convert the pickup and dropoff columns to datetime
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
        df['pickup_day_of_week'] = df['tpep_pickup_datetime'].dt.day_name()

        #Convert data types
        if 'passenger_count' in df.columns:
            df['passenger_count'] = df['passenger_count'].fillna(0).astype(int)
        if 'payment_type' in df.columns:
            df['payment_type'] = df['payment_type'].astype(str)

        #Selecting only the columns defined in the schema
        required_columns = [
            'VendorID', 
            'tpep_pickup_datetime',
            'tpep_dropoff_datetime',
            'passenger_count',
            'trip_distance',
            'payment_type',
            'fare_amount',
            'tip_amount',
            'total_amount'
        ]
        df = df[required_columns]

    elif taxi_type == "green":

        #Convert the pickup and dropoff columns to datetime
        df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
        df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
        df['pickup_day_of_week'] = df['lpep_pickup_datetime'].dt.day_name()

        #Convert data types
        if 'passenger_count' in df.columns:
            df['passenger_count'] = df['passenger_count'].fillna(0).astype(int)
        if 'payment_type' in df.columns:
            df['payment_type'] = df['payment_type'].astype(str)

        #Selecting only the columns defined in the schema
        required_columns = [
            'VendorID', 
            'lpep_pickup_datetime',
            'lpep_dropoff_datetime',
            'passenger_count',
            'trip_distance',
            'payment_type',
            'fare_amount',
            'tip_amount',
            'total_amount'
        ]
        df = df[required_columns]

    else:
        raise ValueError("Could not determine the taxi type")
    


        #Drop rows with invalid total amount values
        df = df[df['Total_amount'] > 0]

    
    print(f"Transformed data shape: {df.shape}")
    return df


def upload_to_bigquery(df, table_id):
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_APPEND)
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    print(f"Data uploaded to BigQuery table {table_id}")

def main(year, month, taxi_type):
    base_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{month:02d}.parquet"
    parquet_file = download_parquet(base_url)
    if parquet_file:
        transformed_data = transform_data(parquet_file, taxi_type)
        table_id = f"ny-taxi-trips-pipeline.ny_taxi_trips.{taxi_type}_taxi"
        upload_to_bigquery(transformed_data, table_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", required=True, type=int, help="Year of the taxi data")
    parser.add_argument("--month", required=True, type=int, help="Month of the taxi data (1-12)")
    parser.add_argument("--taxi-type", required=True, help="Type of taxi (yellow, green)")
    args = parser.parse_args()

    main(args.year, args.month, args.taxi_type)
