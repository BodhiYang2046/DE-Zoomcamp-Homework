provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

resource "google_bigquery_dataset" "my_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}

resource "google_storage_bucket" "parquet_bucket" {
  name     =  var.gcs_bucket_name
  location = "us-central1"
}