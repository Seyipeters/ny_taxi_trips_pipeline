terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
  required_version = ">= 0.13"
}

provider "google" {
  credentials = file("C:/Users/Omole Peter/Desktop/ny_taxi_trips_terraform/ny-taxi-trips-pipeline-9640b65ea078.json")  # Use relative path for portability
  project     = "ny-taxi-trips-pipeline"
  region      = "us-central1"
}

# Create a BigQuery dataset for NYC Taxi trips
resource "google_bigquery_dataset" "ny_taxi_trips" {
  dataset_id = "ny_taxi_trips"
  project    = "ny-taxi-trips-pipeline"
  location   = "US"
}

# Create the Yellow Taxi trips table
resource "google_bigquery_table" "yellow_taxi" {
  dataset_id = google_bigquery_dataset.ny_taxi_trips.dataset_id
  table_id   = "yellow_taxi"
  deletion_protection = false
  schema     = file("${path.module}/schemas/yellow_taxi_schema.json")  # Relative path for schema file
  time_partitioning {
    type = "DAY"
  }
}

# Create the Green Taxi trips table
resource "google_bigquery_table" "green_taxi" {
  dataset_id = google_bigquery_dataset.ny_taxi_trips.dataset_id
  table_id   = "green_taxi"
  deletion_protection = false
  schema     = file("${path.module}/schemas/green_taxi_schema.json")  # Relative path for schema file
  time_partitioning {
    type = "DAY"
  }
}
