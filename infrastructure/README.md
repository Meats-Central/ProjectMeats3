# ProjectMeats3 Infrastructure as Code (IaC)

This directory contains Terraform configurations for provisioning DigitalOcean infrastructure for the ProjectMeats3 application.

## Overview

**What this provisions:**
- DigitalOcean Droplets (Ubuntu VMs) for hosting the application
- Managed PostgreSQL databases for data storage
- Firewall rules for secure database access
- Environment-specific configurations (dev/staging/prod)

**Why use this?**
- **Repeatability**: Recreate identical environments
- **Version Control**: Track infrastructure changes in Git
- **Automation**: Integrate with CI/CD pipelines
- **Control**: Fine-tune resources and configurations

## Directory Structure

```
infrastructure/
├── README.md                     # This file
├── provider.tf                   # Global provider configuration
├── variables.tf                  # Global variables
├── modules/
│   └── app_infra/               # Reusable infrastructure module
│       ├── main.tf              # Core resources (Droplet + Database)
│       ├── variables.tf         # Module input variables
│       ├── outputs.tf           # Module outputs
│       └── user_data.sh         # Cloud-init script for Droplet setup
└── environments/                # Environment-specific configurations
    ├── dev/                     # Development environment
    │   ├── main.tf              # Dev environment setup
    │   ├── provider.tf          # Provider configuration
    │   ├── variables.tf         # Variable definitions
    │   └── dev.tfvars           # Dev-specific values
    ├── staging/                 # Staging environment
    │   ├── main.tf              # Staging environment setup
    │   ├── provider.tf          # Provider configuration
    │   ├── variables.tf         # Variable definitions
    │   └── staging.tfvars       # Staging-specific values
    └── prod/                    # Production environment
        ├── main.tf              # Production environment setup
        ├── provider.tf          # Provider configuration
        ├── variables.tf         # Variable definitions
        └── prod.tfvars          # Production-specific values
```

## Quick Start

### Prerequisites
1. **Terraform installed** (v1.0+)
2. **DigitalOcean account** with API access
3. **SSH key** added to DigitalOcean

### Setup Instructions

1. **Configure access:**
   ```bash
   export TF_VAR_do_token="your-digitalocean-api-token"
   export TF_VAR_ssh_key_id="your-ssh-key-id"
   ```

2. **Choose environment and deploy:**
   ```bash
   cd environments/dev  # or staging/prod
   terraform init
   terraform plan -var-file=dev.tfvars
   terraform apply -var-file=dev.tfvars
   ```

3. **Get connection details:**
   ```bash
   terraform output
   ```

## Environment Configurations

| Environment | Droplet Size | Database | Node Count | Use Case |
|-------------|--------------|----------|------------|-----------|
| **dev** | s-1vcpu-1gb | db-s-1vcpu-1gb | 1 | Development & testing |
| **staging** | s-1vcpu-2gb | db-s-1vcpu-1gb | 1 | Pre-production testing |
| **prod** | s-2vcpu-4gb | db-s-2vcpu-4gb | 2 | Production workloads |

## Resources Created

### DigitalOcean Droplet
- **OS**: Ubuntu 22.04 LTS
- **Region**: NYC3 (configurable)
- **Features**: Docker, Docker Compose, Git pre-installed
- **Application**: Automatically clones and sets up ProjectMeats3

### Managed PostgreSQL Database
- **Version**: PostgreSQL 14
- **Region**: NYC3 (same as Droplet)
- **Database**: `meats_db` automatically created
- **Security**: Firewall configured for Droplet access only

### Security Features
- Database firewall restricts access to application server only
- SSH key authentication for server access
- UFW firewall configured on Droplet
- SSL/TLS encryption for database connections

## Usage Examples

### Deploy Development Environment
```bash
cd environments/dev
terraform init
terraform plan -var-file=dev.tfvars
terraform apply -var-file=dev.tfvars
```

### Scale Production Environment
```bash
cd environments/prod
# Edit prod.tfvars to change droplet_size
terraform plan -var-file=prod.tfvars
terraform apply -var-file=prod.tfvars
```

### Destroy Environment (Cleanup)
```bash
terraform destroy -var-file=<env>.tfvars
```

### Get Database Connection String
```bash
terraform output -raw db_uri
```

## Customization

### Modify Resource Sizes
Edit the `.tfvars` files in each environment directory:
```hcl
droplet_size = "s-2vcpu-4gb"  # Upgrade Droplet
db_size      = "db-s-2vcpu-4gb"  # Upgrade Database
```

### Change Regions
Edit `modules/app_infra/main.tf`:
```hcl
resource "digitalocean_droplet" "app_server" {
  region = "sfo3"  # Change from nyc3 to sfo3
}

resource "digitalocean_database_cluster" "postgres" {
  region = "sfo3"  # Must match Droplet region
}
```

## Monitoring & Maintenance

### Check Resource Status
```bash
terraform show
terraform state list
```

### Update Infrastructure
```bash
terraform plan -var-file=<env>.tfvars
terraform apply -var-file=<env>.tfvars
```

### Backup State Files
Terraform state files contain sensitive information. Consider using remote state storage for production:
```hcl
terraform {
  backend "s3" {
    # Configure remote state storage
  }
}
```

## Troubleshooting

### Common Issues

**Authentication errors:**
- Verify DigitalOcean API token has correct permissions
- Ensure environment variables are set correctly

**Resource creation failures:**
- Check DigitalOcean account limits and quotas
- Verify SSH key exists in DigitalOcean account
- Ensure chosen region supports all resource types

**Application deployment issues:**
- SSH to Droplet and check `/var/log/cloud-init.log`
- Verify database connection in application configuration
- Check Docker services: `docker-compose ps`

### Support Resources

- **Terraform DigitalOcean Provider**: https://registry.terraform.io/providers/digitalocean/digitalocean
- **DigitalOcean API Documentation**: https://docs.digitalocean.com/reference/api/
- **ProjectMeats3 Issues**: https://github.com/Meats-Central/ProjectMeats3/issues

## Cost Estimates

| Environment | Monthly Cost (Approximate) |
|-------------|---------------------------|
| **Development** | $20-25 |
| **Staging** | $25-30 |
| **Production** | $35-45 |

*Costs include Droplet, managed database, and standard networking. Actual costs may vary based on usage and additional features.*

## Next Steps

After successful deployment:

1. **Configure DNS** (if using custom domain)
2. **Set up monitoring** and alerting
3. **Configure backups** for database
4. **Set up CI/CD** integration
5. **Implement remote state** storage for production

For detailed deployment instructions, see the main [USER_DEPLOYMENT_GUIDE.md](../USER_DEPLOYMENT_GUIDE.md).