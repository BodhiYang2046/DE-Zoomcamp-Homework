terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = "./keys/my-creds.json"
  project     = "crested-axe-412222"
  region      = "us-central1"
}


resource "google_storage_bucket" "demo-bucket" {
  name          = "crested-axe-412222-terra-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}



resource "google_bigquery_dataset" "demo-dataset" {
  dataset_id = "demo_dataset"
}