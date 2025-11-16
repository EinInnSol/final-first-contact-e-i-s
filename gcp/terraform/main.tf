# First Contact EIS - GCP Infrastructure
# This Terraform configuration provisions all required GCP resources

terraform {
  required_version = ">= 1.5"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    # Bucket will be created by bootstrap script
    bucket = var.project_id
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "compute.googleapis.com",
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
    "sqladmin.googleapis.com",
    "redis.googleapis.com",
    "cloudtasks.googleapis.com",
    "secretmanager.googleapis.com",
    "storage.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com",
    "cloudscheduler.googleapis.com",
    "vpcaccess.googleapis.com",
    "servicenetworking.googleapis.com",
  ])

  service            = each.value
  disable_on_destroy = false
}

# VPC Network for private resources
resource "google_compute_network" "vpc" {
  name                    = "${var.project_name}-vpc"
  auto_create_subnetworks = false

  depends_on = [google_project_service.required_apis]
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.project_name}-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id

  private_ip_google_access = true
}

# VPC Connector for Cloud Run to access private resources
resource "google_vpc_access_connector" "connector" {
  name          = "${var.project_name}-connector"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.8.0.0/28"

  depends_on = [google_project_service.required_apis]
}

# Cloud SQL PostgreSQL Instance
resource "google_sql_database_instance" "postgres" {
  name             = "${var.project_name}-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier              = var.db_tier
    availability_type = var.environment == "production" ? "REGIONAL" : "ZONAL"

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "03:00"
      transaction_log_retention_days = 7
      backup_retention_settings {
        retained_backups = 7
      }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
      require_ssl     = true
    }

    database_flags {
      name  = "max_connections"
      value = "100"
    }

    insights_config {
      query_insights_enabled  = true
      query_plans_per_minute  = 5
      query_string_length     = 1024
      record_application_tags = true
    }
  }

  deletion_protection = var.environment == "production" ? true : false

  depends_on = [google_service_networking_connection.private_vpc_connection]
}

resource "google_sql_database" "database" {
  name     = var.db_name
  instance = google_sql_database_instance.postgres.name
}

resource "google_sql_user" "db_user" {
  name     = var.db_user
  instance = google_sql_database_instance.postgres.name
  password = random_password.db_password.result
}

# Cloud Memorystore Redis Instance
resource "google_redis_instance" "cache" {
  name           = "${var.project_name}-cache"
  tier           = var.environment == "production" ? "STANDARD_HA" : "BASIC"
  memory_size_gb = var.redis_memory_gb
  region         = var.region

  authorized_network = google_compute_network.vpc.id
  connect_mode       = "PRIVATE_SERVICE_ACCESS"

  redis_version = "REDIS_7_0"
  display_name  = "First Contact EIS Cache"

  depends_on = [google_project_service.required_apis]
}

# Private VPC Connection for Cloud SQL
resource "google_compute_global_address" "private_ip_address" {
  name          = "${var.project_name}-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]

  depends_on = [google_project_service.required_apis]
}

# Artifact Registry for container images
resource "google_artifact_registry_repository" "containers" {
  location      = var.region
  repository_id = "${var.project_name}-images"
  description   = "First Contact EIS container images"
  format        = "DOCKER"

  depends_on = [google_project_service.required_apis]
}

# Cloud Storage bucket for static assets and backups
resource "google_storage_bucket" "assets" {
  name          = "${var.project_id}-assets"
  location      = var.region
  force_destroy = var.environment != "production"

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }

  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD", "PUT", "POST"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

# Secret Manager secrets
resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "random_password" "jwt_secret" {
  length  = 64
  special = true
}

resource "google_secret_manager_secret" "db_password" {
  secret_id = "db-password"

  replication {
    auto {}
  }

  depends_on = [google_project_service.required_apis]
}

resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = random_password.db_password.result
}

resource "google_secret_manager_secret" "jwt_secret" {
  secret_id = "jwt-secret"

  replication {
    auto {}
  }

  depends_on = [google_project_service.required_apis]
}

resource "google_secret_manager_secret_version" "jwt_secret" {
  secret      = google_secret_manager_secret.jwt_secret.id
  secret_data = random_password.jwt_secret.result
}

# Cloud Tasks queue for background jobs
resource "google_cloud_tasks_queue" "default" {
  name     = "${var.project_name}-tasks"
  location = var.region

  rate_limits {
    max_concurrent_dispatches = 100
    max_dispatches_per_second = 500
  }

  retry_config {
    max_attempts       = 5
    max_retry_duration = "4s"
    max_backoff        = "3600s"
    min_backoff        = "5s"
  }

  depends_on = [google_project_service.required_apis]
}

# Cloud Run service for Backend API
resource "google_cloud_run_v2_service" "backend" {
  name     = "${var.project_name}-backend"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      min_instance_count = var.environment == "production" ? 1 : 0
      max_instance_count = var.max_instances
    }

    vpc_access {
      connector = google_vpc_access_connector.connector.id
      egress    = "PRIVATE_RANGES_ONLY"
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.containers.repository_id}/backend:latest"

      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
        cpu_idle = true
      }

      env {
        name  = "DATABASE_URL"
        value = "postgresql://${var.db_user}:${random_password.db_password.result}@${google_sql_database_instance.postgres.private_ip_address}:5432/${var.db_name}"
      }

      env {
        name  = "REDIS_URL"
        value = "redis://${google_redis_instance.cache.host}:${google_redis_instance.cache.port}"
      }

      env {
        name = "SECRET_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.jwt_secret.secret_id
            version = "latest"
          }
        }
      }

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }

      env {
        name  = "GCP_PROJECT"
        value = var.project_id
      }

      startup_probe {
        http_get {
          path = "/health"
        }
        initial_delay_seconds = 10
        period_seconds        = 3
        timeout_seconds       = 1
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = "/health"
        }
        period_seconds    = 10
        timeout_seconds   = 1
        failure_threshold = 3
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [
    google_vpc_access_connector.connector,
    google_sql_database_instance.postgres,
    google_redis_instance.cache
  ]
}

# Cloud Run services for frontends
resource "google_cloud_run_v2_service" "client" {
  name     = "${var.project_name}-client"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      min_instance_count = var.environment == "production" ? 1 : 0
      max_instance_count = var.max_instances
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.containers.repository_id}/client:latest"

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        cpu_idle = true
      }

      env {
        name  = "NEXT_PUBLIC_API_URL"
        value = google_cloud_run_v2_service.backend.uri
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

resource "google_cloud_run_v2_service" "caseworker" {
  name     = "${var.project_name}-caseworker"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      min_instance_count = var.environment == "production" ? 1 : 0
      max_instance_count = var.max_instances
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.containers.repository_id}/caseworker:latest"

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        cpu_idle = true
      }

      env {
        name  = "NEXT_PUBLIC_API_URL"
        value = google_cloud_run_v2_service.backend.uri
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

resource "google_cloud_run_v2_service" "city" {
  name     = "${var.project_name}-city"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      min_instance_count = var.environment == "production" ? 1 : 0
      max_instance_count = var.max_instances
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.containers.repository_id}/city:latest"

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        cpu_idle = true
      }

      env {
        name  = "NEXT_PUBLIC_API_URL"
        value = google_cloud_run_v2_service.backend.uri
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

resource "google_cloud_run_v2_service" "kiosk" {
  name     = "${var.project_name}-kiosk"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      min_instance_count = var.environment == "production" ? 1 : 0
      max_instance_count = var.max_instances
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.containers.repository_id}/kiosk:latest"

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        cpu_idle = true
      }

      env {
        name  = "NEXT_PUBLIC_API_URL"
        value = google_cloud_run_v2_service.backend.uri
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

resource "google_cloud_run_v2_service" "admin" {
  name     = "${var.project_name}-admin"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      min_instance_count = var.environment == "production" ? 1 : 0
      max_instance_count = var.max_instances
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.containers.repository_id}/admin:latest"

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        cpu_idle = true
      }

      env {
        name  = "NEXT_PUBLIC_API_URL"
        value = google_cloud_run_v2_service.backend.uri
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# IAM permissions for Cloud Run services to access secrets
resource "google_secret_manager_secret_iam_member" "backend_jwt_access" {
  secret_id = google_secret_manager_secret.jwt_secret.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_cloud_run_v2_service.backend.template[0].service_account}"
}

resource "google_secret_manager_secret_iam_member" "backend_db_access" {
  secret_id = google_secret_manager_secret.db_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_cloud_run_v2_service.backend.template[0].service_account}"
}

# Cloud Scheduler for periodic tasks
resource "google_cloud_scheduler_job" "cleanup" {
  name             = "${var.project_name}-cleanup"
  description      = "Daily cleanup and maintenance tasks"
  schedule         = "0 2 * * *"
  time_zone        = "America/Los_Angeles"
  attempt_deadline = "320s"
  region           = var.region

  http_target {
    http_method = "POST"
    uri         = "${google_cloud_run_v2_service.backend.uri}/tasks/cleanup"

    oidc_token {
      service_account_email = google_cloud_run_v2_service.backend.template[0].service_account
    }
  }

  depends_on = [google_project_service.required_apis]
}

# Cloud Monitoring alert policies
resource "google_monitoring_alert_policy" "high_error_rate" {
  display_name = "High Error Rate - ${var.project_name}"
  combiner     = "OR"

  conditions {
    display_name = "Error rate above 5%"

    condition_threshold {
      filter          = "resource.type=\"cloud_run_revision\" AND metric.type=\"run.googleapis.com/request_count\" AND metric.label.response_code_class=\"5xx\""
      duration        = "60s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0.05

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  notification_channels = var.alert_email != "" ? [google_monitoring_notification_channel.email[0].name] : []

  alert_strategy {
    auto_close = "1800s"
  }
}

resource "google_monitoring_notification_channel" "email" {
  count        = var.alert_email != "" ? 1 : 0
  display_name = "Email Notification Channel"
  type         = "email"

  labels = {
    email_address = var.alert_email
  }
}

# Cloud Load Balancer (optional, for custom domain)
resource "google_compute_global_address" "lb_ip" {
  count = var.custom_domain != "" ? 1 : 0
  name  = "${var.project_name}-lb-ip"
}

# Outputs
output "backend_url" {
  value       = google_cloud_run_v2_service.backend.uri
  description = "Backend API URL"
}

output "client_url" {
  value       = google_cloud_run_v2_service.client.uri
  description = "Client Portal URL"
}

output "caseworker_url" {
  value       = google_cloud_run_v2_service.caseworker.uri
  description = "Caseworker Dashboard URL"
}

output "city_url" {
  value       = google_cloud_run_v2_service.city.uri
  description = "City Analytics URL"
}

output "kiosk_url" {
  value       = google_cloud_run_v2_service.kiosk.uri
  description = "Kiosk Interface URL"
}

output "admin_url" {
  value       = google_cloud_run_v2_service.admin.uri
  description = "Admin Dashboard URL"
}

output "database_connection" {
  value       = google_sql_database_instance.postgres.private_ip_address
  description = "Cloud SQL private IP"
  sensitive   = true
}

output "redis_host" {
  value       = google_redis_instance.cache.host
  description = "Redis host"
  sensitive   = true
}

output "artifact_registry" {
  value       = google_artifact_registry_repository.containers.name
  description = "Artifact Registry repository"
}
