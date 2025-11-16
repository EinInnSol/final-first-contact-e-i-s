# Variables for First Contact EIS GCP Infrastructure

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "firstcontact-eis"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment (development, staging, production)"
  type        = string
  default     = "development"

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "db_tier" {
  description = "Cloud SQL instance tier"
  type        = string
  default     = "db-f1-micro"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "firstcontact_eis"
}

variable "db_user" {
  description = "Database user"
  type        = string
  default     = "firstcontact"
}

variable "redis_memory_gb" {
  description = "Redis memory size in GB"
  type        = number
  default     = 1
}

variable "max_instances" {
  description = "Maximum number of Cloud Run instances"
  type        = number
  default     = 10
}

variable "alert_email" {
  description = "Email for monitoring alerts"
  type        = string
  default     = ""
}

variable "custom_domain" {
  description = "Custom domain for load balancer"
  type        = string
  default     = ""
}
