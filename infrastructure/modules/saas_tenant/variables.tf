# Multi-Tenant SaaS Infrastructure Variables

variable "tenant_name" {
  description = "Name of the tenant (used for resource naming)"
  type        = string
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]*[a-z0-9]$", var.tenant_name))
    error_message = "Tenant name must be lowercase, start with a letter, and contain only letters, numbers, and hyphens."
  }
}

variable "environment" {
  description = "Environment (development, staging, production)"
  type        = string
  default     = "production"
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be one of: development, staging, production."
  }
}

# Database Configuration
variable "database_size" {
  description = "Database cluster size"
  type        = string
  default     = "db-s-1vcpu-1gb"
}

variable "database_nodes" {
  description = "Number of database nodes"
  type        = number
  default     = 1
}

variable "database_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "15"
}

# App Platform Configuration
variable "app_instance_count" {
  description = "Number of app instances"
  type        = number
  default     = 2
}

variable "app_instance_size" {
  description = "App instance size"
  type        = string
  default     = "basic-xxs"
}

# Domain Configuration
variable "custom_domain" {
  description = "Custom domain for the application"
  type        = string
  default     = null
}

# Feature Flags
variable "enable_redis" {
  description = "Enable Redis for caching"
  type        = bool
  default     = true
}

variable "enable_spaces" {
  description = "Enable DigitalOcean Spaces for object storage"
  type        = bool
  default     = true
}

variable "enable_cdn" {
  description = "Enable CDN for static assets"
  type        = bool
  default     = false
}

variable "enable_monitoring" {
  description = "Enable enhanced monitoring and alerting"
  type        = bool
  default     = true
}

# Resource Tags
variable "tags" {
  description = "Additional tags for resources"
  type        = map(string)
  default     = {}
}

# Subscription Plan Mapping
variable "subscription_plan" {
  description = "Subscription plan tier (affects resource allocation)"
  type        = string
  default     = "basic"
  validation {
    condition     = contains(["free", "basic", "professional", "enterprise"], var.subscription_plan)
    error_message = "Subscription plan must be one of: free, basic, professional, enterprise."
  }
}

# Plan-based resource configurations
locals {
  plan_configs = {
    free = {
      app_instance_count = 1
      app_instance_size  = "basic-xxs"
      database_size      = "db-s-1vcpu-1gb"
      database_nodes     = 1
      enable_redis       = false
      enable_spaces      = false
      enable_cdn         = false
    }
    basic = {
      app_instance_count = 1
      app_instance_size  = "basic-xs"
      database_size      = "db-s-1vcpu-2gb"
      database_nodes     = 1
      enable_redis       = true
      enable_spaces      = true
      enable_cdn         = false
    }
    professional = {
      app_instance_count = 2
      app_instance_size  = "professional-xs"
      database_size      = "db-s-2vcpu-4gb"
      database_nodes     = 2
      enable_redis       = true
      enable_spaces      = true
      enable_cdn         = true
    }
    enterprise = {
      app_instance_count = 3
      app_instance_size  = "professional-s"
      database_size      = "db-s-4vcpu-8gb"
      database_nodes     = 3
      enable_redis       = true
      enable_spaces      = true
      enable_cdn         = true
    }
  }
  
  # Merge plan config with user overrides
  effective_config = merge(
    local.plan_configs[var.subscription_plan],
    {
      app_instance_count = var.app_instance_count
      app_instance_size  = var.app_instance_size
      database_size      = var.database_size
      database_nodes     = var.database_nodes
      enable_redis       = var.enable_redis
      enable_spaces      = var.enable_spaces
      enable_cdn         = var.enable_cdn
    }
  )
}