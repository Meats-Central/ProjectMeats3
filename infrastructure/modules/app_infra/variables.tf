variable "env" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "droplet_size" {
  description = "DigitalOcean droplet size"
  type        = string
}

variable "db_size" {
  description = "DigitalOcean database cluster size"
  type        = string
}

variable "ssh_key_id" {
  description = "DigitalOcean SSH key ID"
  type        = string
}