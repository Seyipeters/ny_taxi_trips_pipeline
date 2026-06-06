# NY Taxi Trips Pipeline

A runnable data engineering project that downloads NYC yellow or green taxi trip data, standardizes the core trip fields, writes a clean output dataset locally, and can optionally append the result to BigQuery.

## What this project demonstrates

- downloading public parquet data from the NYC Taxi and Limousine Commission feed
- cleaning and standardizing trip records with Python and pandas
- exporting analytics-ready data to local parquet or CSV
- optionally loading the transformed dataset into BigQuery
- packaging the workflow in Docker without hard-coding cloud credentials

## Tech stack

- Python
- pandas
- pyarrow
- Docker
- Google BigQuery (optional destination)

## Repository structure

```text
ny_taxi_trips_pipeline/
├── .gitignore
├── Dockerfile
├── ingest_taxi_data.py
├── README.md
├── requirements.txt
└── terraform/
	├── main.tf
	├── variables.tf
	├── outputs.tf
	└── schemas/
		├── yellow_taxi_schema.json
		└── green_taxi_schema.json
```

## Pipeline flow

1. Download the source parquet file for a chosen taxi type, year, and month.
2. Keep the core trip columns used for analysis.
3. Normalize timestamps and numeric fields.
4. Drop invalid rows with missing required values or non-positive totals.
5. Save the cleaned dataset locally.
6. Optionally append the same dataset to a BigQuery table.

## Local usage

### Prerequisites

- Python 3.9+
- `pip install -r requirements.txt`

### Save transformed data locally

```powershell
python ingest_taxi_data.py --year 2024 --month 1 --taxi-type yellow
```

This writes a parquet file to `data/processed/` by default.

### Save as CSV to a custom directory

```powershell
python ingest_taxi_data.py --year 2024 --month 1 --taxi-type green --output-format csv --output-dir output
```

### Load to BigQuery

Make sure your local environment is already authenticated for Google Cloud, then run:

```powershell
python ingest_taxi_data.py --year 2024 --month 1 --taxi-type yellow --table-id your-project.your_dataset.yellow_taxi
```

### Provision BigQuery infrastructure with Terraform

```powershell
cd terraform
terraform init
terraform apply -var="project_id=your-project" -var="dataset_id=ny_taxi_trips"
```

## Docker usage

Build the image:

```powershell
docker build -t ny-taxi-loader .
```

Run the pipeline and write output into a local folder:

```powershell
docker run --rm -v ${PWD}/data:/app/data ny-taxi-loader --year 2024 --month 1 --taxi-type yellow
```

If you want BigQuery loading from Docker, mount your Google credentials and set `GOOGLE_APPLICATION_CREDENTIALS` at runtime instead of baking secrets into the image.

## Recruiter-facing project value

This project is useful in a data engineering portfolio because it shows:

- ingestion from a public source
- data cleaning and schema control
- configurable outputs for batch processing
- optional cloud warehouse loading without embedding credentials in source control

## Next improvements

- add automated tests for the transform function
- parameterize partitioned BigQuery table creation
- add orchestration with a scheduler such as Airflow or Prefect
- add data quality assertions and row-count checks

