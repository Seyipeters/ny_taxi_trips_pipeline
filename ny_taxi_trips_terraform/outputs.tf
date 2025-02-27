output "bigquery_dataset_id" {
    description = "The BigQuery dataset ID creared"
    value = google_bigquery_dataset.ny_taxi_trips.dataset_id
}

output "yellow_table_taxi_id" {
    description = "Yellow Taxi BigQuery table name"
    value = google_bigquery_table.yellow_taxi.table_id
}

output "green_table_taxi_id" {
    description = "Green Taxi BigQuery table name"
    value = google_bigquery_table.green_taxi.table_id
}