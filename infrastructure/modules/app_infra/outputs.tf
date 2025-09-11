output "droplet_ip" {
  description = "IP address of the application server"
  value       = digitalocean_droplet.app_server.ipv4_address
}

output "db_uri" {
  description = "PostgreSQL connection URI"
  value       = digitalocean_database_cluster.postgres.uri
  sensitive   = true
}

output "db_host" {
  description = "PostgreSQL host address"
  value       = digitalocean_database_cluster.postgres.host
}

output "db_port" {
  description = "PostgreSQL port"
  value       = digitalocean_database_cluster.postgres.port
}

output "db_database" {
  description = "PostgreSQL database name"
  value       = digitalocean_database_db.app_db.name
}

output "db_user" {
  description = "PostgreSQL username"
  value       = digitalocean_database_cluster.postgres.user
  sensitive   = true
}

output "db_password" {
  description = "PostgreSQL password"
  value       = digitalocean_database_cluster.postgres.password
  sensitive   = true
}