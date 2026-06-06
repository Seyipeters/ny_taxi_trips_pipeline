import argparse
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests


TIMESTAMP_COLUMNS = {
    "yellow": {
        "pickup": "tpep_pickup_datetime",
        "dropoff": "tpep_dropoff_datetime",
    },
    "green": {
        "pickup": "lpep_pickup_datetime",
        "dropoff": "lpep_dropoff_datetime",
    },
}


def download_parquet(url: str) -> BytesIO:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    print(f"Downloaded data from {url}")
    return BytesIO(response.content)


def transform_data(parquet_file: BytesIO, taxi_type: str) -> pd.DataFrame:
    if taxi_type not in TIMESTAMP_COLUMNS:
        raise ValueError("taxi_type must be 'yellow' or 'green'")

    df = pd.read_parquet(parquet_file)
    pickup_column = TIMESTAMP_COLUMNS[taxi_type]["pickup"]
    dropoff_column = TIMESTAMP_COLUMNS[taxi_type]["dropoff"]

    required_columns = [
        "VendorID",
        pickup_column,
        dropoff_column,
        "passenger_count",
        "trip_distance",
        "payment_type",
        "fare_amount",
        "tip_amount",
        "total_amount",
    ]
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = df[required_columns].copy()
    df[pickup_column] = pd.to_datetime(df[pickup_column], errors="coerce")
    df[dropoff_column] = pd.to_datetime(df[dropoff_column], errors="coerce")

    numeric_columns = ["passenger_count", "trip_distance", "fare_amount", "tip_amount", "total_amount"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["payment_type"] = df["payment_type"].fillna("unknown").astype(str)
    df["passenger_count"] = df["passenger_count"].fillna(0).astype(int)
    df = df.dropna(subset=[pickup_column, dropoff_column, "trip_distance", "fare_amount", "tip_amount", "total_amount"])
    df = df[df["total_amount"] > 0].copy()
    df["pickup_day_of_week"] = df[pickup_column].dt.day_name()
    df["pickup_year"] = df[pickup_column].dt.year
    df["pickup_month"] = df[pickup_column].dt.month
    df["taxi_type"] = taxi_type

    print(f"Transformed data shape: {df.shape}")
    return df


def save_output(df: pd.DataFrame, output_dir: Path, taxi_type: str, year: int, month: int, output_format: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{taxi_type}_taxi_{year}_{month:02d}.{output_format}"

    if output_format == "parquet":
        df.to_parquet(output_path, index=False)
    elif output_format == "csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("output_format must be 'parquet' or 'csv'")

    print(f"Saved transformed data to {output_path}")
    return output_path


def upload_to_bigquery(df: pd.DataFrame, table_id: str) -> None:
    from google.cloud import bigquery

    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_APPEND)
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    print(f"Uploaded data to BigQuery table {table_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download, transform, and optionally load NYC taxi trip data.")
    parser.add_argument("--year", required=True, type=int, help="Year of the taxi data")
    parser.add_argument("--month", required=True, type=int, help="Month of the taxi data (1-12)")
    parser.add_argument("--taxi-type", required=True, choices=["yellow", "green"], help="Type of taxi data to ingest")
    parser.add_argument("--output-dir", default="data/processed", help="Directory for the transformed output file")
    parser.add_argument("--output-format", default="parquet", choices=["parquet", "csv"], help="Output file format")
    parser.add_argument("--table-id", help="Optional BigQuery table ID in the form project.dataset.table")
    args = parser.parse_args()

    source_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{args.taxi_type}_tripdata_{args.year}-{args.month:02d}.parquet"
    parquet_file = download_parquet(source_url)
    transformed_data = transform_data(parquet_file, args.taxi_type)
    save_output(transformed_data, Path(args.output_dir), args.taxi_type, args.year, args.month, args.output_format)

    if args.table_id:
        upload_to_bigquery(transformed_data, args.table_id)


if __name__ == "__main__":
    main()
