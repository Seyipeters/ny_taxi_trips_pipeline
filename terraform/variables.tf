variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud region"
  type        = string
  default     = "us-central1"
}

variable "dataset_id" {
  description = "BigQuery dataset ID for taxi tables"
  type        = string
  default     = "ny_taxi_trips"
}

variable "dataset_location" {
  description = "BigQuery dataset location"
  type        = string
  default     = "US"
}
