module "app_infra" {
  source       = "../../modules/app_infra"
  env          = "staging"
  droplet_size = "s-1vcpu-2gb"
  db_size      = "db-s-1vcpu-1gb"
  ssh_key_id   = var.ssh_key_id
}

output "droplet_ip" {
  description = "Staging server IP address"
  value       = module.app_infra.droplet_ip
}

output "db_connection_info" {
  description = "Database connection information"
  value = {
    host     = module.app_infra.db_host
    port     = module.app_infra.db_port
    database = module.app_infra.db_database
    user     = module.app_infra.db_user
  }
  sensitive = true
}