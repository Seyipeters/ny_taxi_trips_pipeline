output "dataset_id" {
  description = "BigQuery dataset ID"
  value       = google_bigquery_dataset.ny_taxi.dataset_id
}

output "yellow_table_id" {
  description = "Fully qualified yellow taxi table"
  value       = "${var.project_id}.${google_bigquery_dataset.ny_taxi.dataset_id}.${google_bigquery_table.yellow_taxi.table_id}"
}

output "green_table_id" {
  description = "Fully qualified green taxi table"
  value       = "${var.project_id}.${google_bigquery_dataset.ny_taxi.dataset_id}.${google_bigquery_table.green_taxi.table_id}"
}
