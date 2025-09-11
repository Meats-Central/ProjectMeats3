terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

resource "digitalocean_droplet" "app_server" {
  image     = "ubuntu-22-04-x64"
  name      = "projectmeats-app-${var.env}"
  region    = "nyc3"
  size      = var.droplet_size
  ssh_keys  = [var.ssh_key_id]
  user_data = file("${path.module}/user_data.sh")

  tags = ["projectmeats", "app", var.env]
}

resource "digitalocean_database_cluster" "postgres" {
  name       = "projectmeats-db-${var.env}"
  engine     = "pg"
  version    = "14"
  size       = var.db_size
  region     = "nyc3"
  node_count = var.env == "prod" ? 2 : 1

  tags = ["projectmeats", "database", var.env]
}

resource "digitalocean_database_db" "app_db" {
  cluster_id = digitalocean_database_cluster.postgres.id
  name       = "meats_db"
}

resource "digitalocean_database_firewall" "db_firewall" {
  cluster_id = digitalocean_database_cluster.postgres.id
  
  rule {
    type  = "ip_addr"
    value = digitalocean_droplet.app_server.ipv4_address
  }
}