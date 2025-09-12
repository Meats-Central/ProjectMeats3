# Multi-Tenant SaaS Infrastructure Module

This module provides infrastructure for multi-tenant deployment of ProjectMeats3.

## Components

- **App Platform**: DigitalOcean App Platform for scalable web application hosting
- **Database**: Managed PostgreSQL cluster with connection pooling
- **Redis**: Managed Redis for caching and session storage  
- **Spaces**: Object storage for file uploads and static assets
- **Load Balancer**: Traffic distribution and SSL termination
- **Monitoring**: DigitalOcean monitoring and alerting

## Usage

```hcl
module "tenant_infrastructure" {
  source = "./modules/saas_tenant"
  
  tenant_name = "acme-corp"
  environment = "production"
  
  # Database configuration
  database_size     = "db-s-2vcpu-2gb"
  database_nodes    = 2
  
  # App configuration
  app_instance_count = 3
  app_instance_size  = "professional-xs"
  
  # Domain configuration
  custom_domain = "acme.projectmeats.com"
  
  # Feature flags
  enable_redis    = true
  enable_spaces   = true
  enable_cdn      = true
}
```

## Outputs

- `app_url`: Application URL
- `database_connection`: Database connection details
- `redis_connection`: Redis connection details (if enabled)
- `spaces_endpoint`: Object storage endpoint (if enabled)