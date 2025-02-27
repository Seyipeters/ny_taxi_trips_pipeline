# NY Taxi ETL Pipeline

This project automates the ETL (Extract, Transform, Load) process for New York City Yellow and Green taxi trip data. The pipeline extracts data in Parquet format from the NYC taxi website, transforms it, and loads it into Google BigQuery for analysis and visualization.

## Table of Contents
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Project Workflow](#project-workflow)
- [Installation & Setup](#installation--setup)
- [BigQuery Optimization Strategies](#bigquery-optimization-strategies)
- [Contributing](#contributing)
- [License](#license)


## Project Structure

```
ny_taxi_trips_pipeline/
├── Dockerfile
├── README.md
├── data/
├── scripts/
│   ├── ingest_taxi_data.py
├── terraform/
│   ├── schemas/
│   │   ├── yellow_taxi_schema.json
│   │   └── green_taxi_schema.json
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
```
ny_taxi_trips_pipeline/
├── Dockerfile
├── README.md
├── data/
├── scripts/
│   ├── ingest_taxi_data.py
├── terraform/
├── schemas/
├── yellow_taxi_schema.json
│   └── green_taxi_schema.json
├── main.tf
├── variables.tf
└── outputs.tf
```

## BigQuery Optimization Strategies

- **Partitioning & Clustering**: Improve query performance and reduce costs.
- **Materialized Views**: Precompute and cache frequent queries.
- **Query Caching**: Utilize BigQuery’s caching mechanism for efficiency.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.
```
```

## Technologies Used

- **Python**: Data extraction and transformation
- **Docker**: Containerized execution of the ETL pipeline
- **Terraform**: Infrastructure as Code (IaC) for cloud resource management
- **Google BigQuery**: Data storage and analysis

## Project Workflow

1. **Extract**: Download NYC taxi data (Yellow and Green taxis) from the NYC Taxi & Limousine Commission website.
2. **Transform**: Process the raw data to ensure consistency and structure before loading.
3. **Load**: Store the transformed data into Google BigQuery.
4. **Analysis**: Utilize BigQuery best practices for optimized queries and cost-effective data processing.
5. **Visualization**: Create dashboards for data insights.

## Installation & Setup

### Prerequisites

Ensure you have the following installed:
- Docker
- Terraform
- Google Cloud SDK (with authentication set up for BigQuery)

### Steps

1. Clone this repository:
    ```sh
    git clone https://github.com/Seyipeters/ny_taxi_trips_pipeline.git
    cd ny_taxi_trips_pipeline
    ```
2. Build and run the Docker container:
    ```sh
    docker build -t ny-taxi-loader .
    docker run --rm ny-taxi-loader --year 2024 --month 1 --taxi-type yellow
    ```
3. Deploy infrastructure with Terraform:
    ```sh
    terraform init
    terraform plan
    terraform apply
    ```
4. Verify data in Google BigQuery and start analysis.

## BigQuery Optimization Strategies

- **Partitioning & Clustering**: Improve query performance and reduce costs.
- **Materialized Views**: Precompute and cache frequent queries.
- **Query Caching**: Utilize BigQuery’s caching mechanism for efficiency.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

