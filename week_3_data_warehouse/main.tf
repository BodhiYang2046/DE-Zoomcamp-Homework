provider "google" {
  project = "green_taxi_trip_2022"
  region  = "us-central1"
}

resource "google_compute_instance" "example" {
  name         = "example-instance"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}

provider "google" {
  credentials = file("path/to/google_credentials.json")
  project     = "your_project_id"
  region      = "your_region"
}

resource "google_storage_bucket" "parquet_bucket" {
  name          = "parquet-bucket-name"
}

resource "google_bigquery_dataset" "parquet_dataset" {
  dataset_id = "parquet_dataset"

  labels = {
    environment = "production"
  }
}

resource "google_bigquery_table" "parquet_table" {
  dataset_id = google_bigquery_dataset.parquet_dataset.dataset_id
  table_id   = "parquet_table"

  schema = <<EOF
[
  {"name": "column1", "type": "INTEGER"},
  {"name": "column2", "type": "STRING"},
  -- Add more columns as needed
]
EOF
}

resource "google_storage_bucket_object" "parquet_objects" {
  bucket = google_storage_bucket.parquet_bucket.name
  count  = 12

  source = "path/to/parquet/files/parquet_file_${count.index + 1}.parquet"
  name   = "parquet_file_${count.index + 1}.parquet"
}

resource "google_bigquery_table_import" "parquet_import" {
  dataset_id       = google_bigquery_dataset.parquet_dataset.dataset_id
  table_id         = google_bigquery_table.parquet_table.table_id
  source_uris      = [for obj in google_storage_bucket_object.parquet_objects : "gs://${google_storage_bucket.parquet_bucket.name}/${obj.name}"]
  schema           = google_bigquery_table.parquet_table.schema
  autodetect       = false
  source_format    = "PARQUET"
  max_bad_records  = 10
  ignore_unknown_values = false
}
