terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_bigquery_dataset" "ny_taxi" {
  dataset_id                 = var.dataset_id
  location                   = var.dataset_location
  delete_contents_on_destroy = true
}

resource "google_bigquery_table" "yellow_taxi" {
  dataset_id          = google_bigquery_dataset.ny_taxi.dataset_id
  table_id            = "yellow_taxi"
  deletion_protection = false
  schema              = file("${path.module}/schemas/yellow_taxi_schema.json")
}

resource "google_bigquery_table" "green_taxi" {
  dataset_id          = google_bigquery_dataset.ny_taxi.dataset_id
  table_id            = "green_taxi"
  deletion_protection = false
  schema              = file("${path.module}/schemas/green_taxi_schema.json")
}
